import itertools
import json
from functools import cmp_to_key
from pathlib import Path

packets_raw: str = Path("day-13-input.txt").read_text().strip()

CORRECT = -1
DUNNO = 0
INCORRECT = 1
DIVIDER_PACKETS = [[[2]], [[6]]]


def compare_iterative(a: list | int, b: list | int) -> int:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return CORRECT
        elif b < a:
            return INCORRECT
        else:
            return DUNNO
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    for i in itertools.count(start=0):
        left = a[i] if i < len(a) else None
        right = b[i] if i < len(b) else None
        if right is None and left is None:
            return DUNNO
        if right is None:
            return INCORRECT
        if left is None:
            return CORRECT
        sub_order = compare_iterative(left, right)
        if sub_order != DUNNO:
            return sub_order
    return DUNNO  # Can't get here, but satisfies mypy


results: dict[int, int] = {}
for i_packet, packet in enumerate(packets_raw.split("\n\n"), start=1):
    a_raw, b_raw = packet.strip().split("\n")
    results[i_packet] = compare_iterative(json.loads(a_raw), json.loads(b_raw))

total = sum(k for k, v in results.items() if v == CORRECT)
print(f"Part 1: sum of correct packet indices is {total}")


packets: list[list] = [
    json.loads(p) for p in packets_raw.split("\n") if p
] + DIVIDER_PACKETS
sorted_results = sorted(packets, key=cmp_to_key(compare_iterative))
decoder_key = (sorted_results.index(DIVIDER_PACKETS[0]) + 1) * (
    sorted_results.index(DIVIDER_PACKETS[1]) + 1
)
print(f"Part 2: decoder key is {decoder_key}")
