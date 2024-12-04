from pathlib import Path

import re


MUL_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")
DONT_PATTERN = re.compile(r"don't\(\).*?do\(\)")
raw_input = Path("03.txt").read_text().strip()


def sum_mul_products(instructions: str) -> int:
    matches = MUL_PATTERN.findall(instructions)
    return sum(map(lambda x: int(x[0]) * int(x[1]), matches))


print(f"Part 1: sum is {sum_mul_products(raw_input)}")
filtered_input = re.sub(DONT_PATTERN, "", raw_input)
print(f"Part 2: sum is {sum_mul_products(filtered_input)}")
