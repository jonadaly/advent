from pathlib import Path
from typing import Callable

import numpy as np

positions_raw = Path("7.txt").read_text().strip().split(",")
positions = list(map(int, positions_raw))
triangle: Callable = np.vectorize(lambda n: (n * (n + 1)) / 2.0)

part1_fuel_costs = {}
part2_fuel_costs = {}
for i in range(min(positions), max(positions) + 1):
    abs_diffs = np.abs(np.subtract(positions, i))
    part1_fuel_costs[i] = sum(abs_diffs)
    part2_fuel_costs[i] = sum(triangle(abs_diffs))

print(f"Part 1: min fuel required is {min(part1_fuel_costs.values())}")
print(f"Part 1: min fuel required is {min(part2_fuel_costs.values())}")
