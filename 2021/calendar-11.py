from pathlib import Path

import numpy as np
from skimage import measure

raw_area = Path("11.txt").read_text().strip().split("\n")

height = len(raw_area)
width = len(raw_area[0])
area = np.ndarray((height, width))
for ind, row in enumerate(raw_area):
    area[ind, :] = list(row)

total_flashes = 0
step = 1
while True:
    area += 1
    is_flash = np.zeros((height, width))
    while True:
        old_flash = is_flash.copy()
        for i_row, row in enumerate(area):
            for i_col, element in enumerate(row):
                if element > 9 and is_flash[i_row, i_col] == 0:
                    is_flash[i_row, i_col] = 1
                    x_min = max(i_col - 1, 0)
                    x_max = min(i_col + 2, len(area[0]))
                    y_min = max(i_row - 1, 0)
                    y_max = min(i_row + 2, len(area))
                    area[y_min:y_max, x_min:x_max] += 1
                    element = 0
        if np.equal(is_flash, old_flash).all():
            break
    total_flashes += np.sum(is_flash)
    area = np.where(area > 9, 0, area)
    if step == 100:
        print(f"Part 1: {total_flashes} total flashes")
    if is_flash.all():
        print(f"Part 2: simulflash at step {step}")
        break
    step += 1
