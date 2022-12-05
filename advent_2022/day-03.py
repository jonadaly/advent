import string
from pathlib import Path

bags: list[str] = Path("day-03-input.txt").read_text().strip().split("\n")
priority: dict[str, int] = {
    v: k for k, v in enumerate(string.ascii_lowercase + string.ascii_uppercase, start=1)
}

total_part1 = sum(
    priority[next(iter(set(bag[: len(bag) // 2]) & set(bag[len(bag) // 2 :])))]
    for bag in bags
)
print(f"Part 1: total priority is {total_part1}")

total_part2 = sum(
    priority[next(iter(set.intersection(*[set(bag) for bag in bags[i : i + 3]])))]
    for i in range(0, len(bags), 3)
)
print(f"Part 2: total priority is {total_part2}")
