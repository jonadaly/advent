from pathlib import Path

import re

raw_input = Path("03.txt").read_text().strip()


def sum_mul_products(instructions: str) -> int:
    matches = mul_pattern.findall(instructions)
    return sum(map(lambda x: int(x[0]) * int(x[1]), matches))


mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
dont_pattern = re.compile(r"don't\(\).*?do\(\)", re.DOTALL)

product_sum = sum_mul_products(raw_input)
print(f"Part 1: sum is {product_sum}")

filtered_input = re.sub(dont_pattern, "", raw_input)
product_sum = sum_mul_products(filtered_input)
print(f"Part 2: sum is {product_sum}")
