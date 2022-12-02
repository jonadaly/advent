import re
from pathlib import Path

raw_instructions = Path("02.txt").read_text().strip().split("\n")

horizontal = 0
depth = 0
aim = 0
for raw_instruction in raw_instructions:
    direction, amount = re.match(r"^(.+) (\d+)$", raw_instruction).groups()
    if direction == "forward":
        horizontal += int(amount)
    elif direction == "down":
        depth += int(amount)
    elif direction == "up":
        depth -= int(amount)
    else:
        raise RuntimeError
print(f"Part 1: horizontal {horizontal} x depth {depth} = {horizontal*depth}")

horizontal = 0
depth = 0
aim = 0
for raw_instruction in raw_instructions:
    direction, amount = re.match(r"^(.+) (\d+)$", raw_instruction).groups()
    if direction == "forward":
        horizontal += int(amount)
        depth += aim * int(amount)
    elif direction == "down":
        aim += int(amount)
    elif direction == "up":
        aim -= int(amount)
    else:
        raise RuntimeError
print(f"Part 2: horizontal {horizontal} x depth {depth} = {horizontal*depth}")
