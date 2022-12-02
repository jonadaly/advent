from pathlib import Path

import numpy as np
from skimage import measure

raw_area = Path("09.txt").read_text().strip().split("\n")

height = len(raw_area)
width = len(raw_area[0])
area = np.ndarray((height, width))
for ind, row in enumerate(raw_area):
    area[ind, :] = list(row)

risk_level = 0
for i_row, row in enumerate(area):
    for i_col, element in enumerate(row):
        is_low = True
        if i_row > 0:
            is_low = is_low and area[i_row - 1, i_col] > element
        if i_row < height - 1:
            is_low = is_low and area[i_row + 1, i_col] > element
        if i_col > 0:
            is_low = is_low and area[i_row, i_col - 1] > element
        if i_col < width - 1:
            is_low = is_low and area[i_row, i_col + 1] > element
        if is_low:
            risk_level += 1 + element

area_basined = (area < 9).astype(int)
labels = measure.label(area_basined, connectivity=1)
props = measure.regionprops(labels)
basin_size = sorted([len(p.coords) for p in props], reverse=True)

print(f"Part 1: risk_level is {risk_level}")
print(
    f"Part 2: product of largest 3 basins is {basin_size[0] * basin_size[1]*basin_size[2]}"
)
