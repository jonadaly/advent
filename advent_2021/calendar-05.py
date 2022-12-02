import re
from pathlib import Path

import numpy as np

vents_raw = Path("05.txt").read_text().strip().split("\n")

vents = []
for vent_raw in vents_raw:
    groups = re.match(r"^(\d+),(\d+) -> (\d+),(\d+)$", vent_raw).groups()
    x_start = int(groups[0])
    y_start = int(groups[1])
    x_end = int(groups[2])
    y_end = int(groups[3])
    vents.append((x_start, y_start, x_end, y_end))

maximum_value = max(
    max(v[0] for v in vents),
    max(v[1] for v in vents),
    max(v[2] for v in vents),
    max(v[3] for v in vents),
)

floor_p1 = np.zeros((maximum_value + 1, maximum_value + 1))
floor_p2 = np.zeros((maximum_value + 1, maximum_value + 1))
for x_start, y_start, x_end, y_end in vents:
    print((x_start, y_start, x_end, y_end))
    x_min = min(x_start, x_end)
    x_max = max(x_start, x_end)
    y_min = min(y_start, y_end)
    y_max = max(y_start, y_end)
    if x_start == x_end:
        floor_p1[y_min : y_max + 1, x_start] += 1
        floor_p2[y_min : y_max + 1, x_start] += 1
    elif y_start == y_end:
        floor_p1[y_start, x_min : x_max + 1] += 1
        floor_p2[y_start, x_min : x_max + 1] += 1
    else:
        # Diagonal vent. Must be 45 degrees.
        for i in range(x_max - x_min + 1):
            floor_p2[
                y_start + i * np.sign(y_end - y_start),
                x_start + i * np.sign(x_end - x_start),
            ] += 1


n_dangerous_p1 = np.sum(floor_p1 >= 2)
n_dangerous_p2 = np.sum(floor_p2 >= 2)
print(f"Part 1: {n_dangerous_p1} tiles are dangerous")
print(f"Part 2: {n_dangerous_p2} tiles are dangerous")
