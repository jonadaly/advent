from pathlib import Path
from collections import defaultdict
import re
import numpy as np
from typing import List

lines = Path("14.txt").read_text().strip().split("\n")

# Part 1
memory = defaultdict(int)
mask = 0
for line in lines:
    if line.startswith("mask"):
        mask = line[7:]
        continue
    address, value = re.match(r"^mem\[(\d+)\] = (\d+)$", line).groups()
    binary_value = '{0:b}'.format(int(value))
    binary_value = "0"*(len(mask) - len(binary_value)) + binary_value
    result = ["0"]*len(binary_value)
    for i, v in enumerate(mask):
        if v == "1":
            result[i] = "1"
        elif v == "0":
            result[i] = "0"
        else:
            result[i] = binary_value[i]
    memory[int(address)] = int(''.join(result), 2)
    # print(f"Mask:\t\t{mask}")
    # print(f"Value:\t\t{binary_value} ({int(binary_value, 2)})")
    # print(f"Result:\t\t{''.join(result)} ({(int(''.join(result), 2))})")
print(f"Part 1: sum is {sum(memory.values())}")
    
# Part 2
def find_poss_addresses(address) -> List[str]:
    results = []
    i_first_x = address.find("X")
    if i_first_x == -1:
        return [address]
    new = list(address)
    new[i_first_x] = '1'
    with_one = ''.join(new)
    new[i_first_x] = '0'
    with_zero = "".join(new)
    results.extend(find_poss_addresses(with_one))
    results.extend(find_poss_addresses(with_zero))
    return results
memory = defaultdict(int)
mask = 0
for line in lines:
    if line.startswith("mask"):
        mask = line[7:]
        continue
    address, value = re.match(r"^mem\[(\d+)\] = (\d+)$", line).groups()
    binary_address = '{0:b}'.format(int(address))
    binary_address = "0"*(len(mask) - len(binary_address)) + binary_address
    result = ["0"]*len(binary_address)
    for i, v in enumerate(mask):
        if v == "1":
            result[i] = "1"
        elif v == "0":
            result[i] = binary_address[i]
        else:
            result[i] = v
    masked_address = "".join(result)
    # print(f"Mask:\t\t{mask}")
    # print(f"Address:\t{binary_address}")
    # print(f"Result:\t\t{masked_address}")
    possible_addresses = find_poss_addresses(masked_address)
    for pa in possible_addresses:
        # print(f"Writing {int(value)} to address {int(pa, 2)}")
        memory[int(pa, 2)] = int(value)
print(f"Part 2: sum is {sum(memory.values())}")