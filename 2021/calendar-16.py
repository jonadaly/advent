import math
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from bitstring import BitArray

packet_raw = Path("16.txt").read_text().strip()

operators = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1]),
}


def parse_first_packet(packet: BitArray, depth: Optional[int] = 1) -> Tuple[int, int]:
    """
    Parses the first packet found and returns a tuple containing the index of the first unparsed bit, and the
    packet value.
    """
    version = packet[:3].uint
    operator = packet[3:6].uint
    global version_total
    version_total += version
    # print(f"{depth*'--'}> parsing packet {packet.bin[:10]}... - v{version}, op {operator}")
    if operator == 4:
        payload = packet[6:]
        value = "0b"
        chunk_start_idx = 0
        while True:
            chunk = payload[chunk_start_idx + 1 : chunk_start_idx + 5]
            value += chunk.bin
            if payload[chunk_start_idx] == 0:
                break
            chunk_start_idx += 5
        # print(f"{depth*'--'}> value is {int(value, 2)}")
        return chunk_start_idx + 5 + 6, int(value, 2)
    else:
        length_type_id = packet[6]
        operator_fn: Callable = operators[operator]
        if length_type_id == 0:
            length_in_bits = packet[7:22].uint
            # print(f"{depth*'--'}> sub-packets length: {length_in_bits} bits")
            _, values = parse_multi_packet(
                packet[22 : 22 + length_in_bits], depth=depth + 1
            )
            return 22 + length_in_bits, operator_fn(values)
        else:
            n_sub_packets = packet[7:18].uint
            # print(f"{depth*'--'}> number of sub-packets: {n_sub_packets}")
            final_pointer, values = parse_multi_packet(
                packet[18:], limit=n_sub_packets, depth=depth + 1
            )
            return 18 + final_pointer, operator_fn(values)


def parse_multi_packet(
    packets: BitArray, limit: Optional[int] = None, depth: Optional[int] = 1
) -> Tuple[int, List[int]]:
    """
    Parses multiple packets and returns a tuple containing the index of the first unparsed bit, and a list of
    values from each packet.
    """
    pointer = 0
    values: List[int] = []
    while True:
        print(
            f"{depth*'--'}> Parsing next packet ({len(values) + 1} of {limit or '?'})"
        )
        end_index, value = parse_first_packet(packets[pointer:], depth=depth)
        pointer += end_index
        values.append(value)
        if pointer >= len(packets):
            return pointer, values
        if limit is not None and len(values) >= limit:
            return pointer, values


version_total = 0
overall_packets = BitArray(hex=packet_raw)
_, overall_values = parse_multi_packet(overall_packets, limit=1, depth=1)
print(f"Part 1: total of version numbers is {version_total}")
print(f"Part 2: overall value is {overall_values[0]}")
