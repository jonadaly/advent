import re
from pathlib import Path

assignments: list[str] = Path("day-04-input.txt").read_text().strip().split("\n")

count_p1 = 0
count_p2 = 0
for assignment in assignments:
    match = re.match(r"(\d+)\-(\d+),(\d+)\-(\d+)", assignment)
    if match is None:
        raise Exception
    elf1_start, elf1_end, elf2_start, elf2_end = tuple(map(int, match.groups()))
    elf1: set[int] = set(range(elf1_start, elf1_end + 1))
    elf2: set[int] = set(range(elf2_start, elf2_end + 1))
    if elf1 >= elf2 or elf2 >= elf1:  # check if either is subset of other
        count_p1 += 1
    if elf1 & elf2:  # check if there is any overlap
        count_p2 += 1

print(f"Part 1: {count_p1} pairs have one range completely containing the other")
print(f"Part 2: {count_p2} pairs have at least some overlap")
