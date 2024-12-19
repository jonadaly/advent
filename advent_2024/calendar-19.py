import functools
from pathlib import Path


towels_available_raw, _, *towels_required = (
    Path("19.txt").read_text().strip().split("\n")
)
towels_available = towels_available_raw.split(", ")


@functools.cache  # Here's the magic
def count_combinations(towel: str) -> int:
    if towel == "":
        return 1
    return sum(
        count_combinations(towel[len(a) :])
        for a in towels_available
        if towel.startswith(a)
    )


combinations = {towel: count_combinations(towel) for towel in towels_required}
solvable = sum(bool(combo) for combo in combinations.values())
sum_combos = sum(combo for combo in combinations.values())

print(f"Part 1: {solvable} towels can be made")
print(f"Part 2: {sum_combos} total combinations can be used to make towels")
