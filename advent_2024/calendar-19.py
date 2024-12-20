import functools
from pathlib import Path


available_raw, _, *required = Path("19.txt").read_text().strip().split("\n")
available = available_raw.split(", ")


@functools.cache  # Here's the magic
def count(towel: str) -> int:
    if towel == "":
        return 1
    return sum(count(towel[len(a) :]) for a in available if towel.startswith(a))


combinations = {towel: count(towel) for towel in required}
solvable = sum(bool(combo) for combo in combinations.values())
sum_combos = sum(combo for combo in combinations.values())

print(f"Part 1: {solvable} towels can be made")
print(f"Part 2: {sum_combos} total combinations can be used to make towels")
