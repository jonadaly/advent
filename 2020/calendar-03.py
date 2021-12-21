from pathlib import Path
import re
import numpy as np


def count_trees(slope_right: int, slope_down: int) -> int:
    idx_row = 0
    idx_col = 0
    n_trees = 0
    while True:
        # print(f"Position: {idx_row}, {idx_col}")
        idx_col += slope_right
        if idx_col >= len(raw_slope[0]):
            idx_col -= len(raw_slope[0])
        idx_row += slope_down
        if idx_row >= len(raw_slope):
            break
        if slope[idx_row, idx_col] == b"#":
            n_trees += 1
    return n_trees


raw_slope = Path("03.txt").read_text().strip().split("\n")

slope = np.chararray((len(raw_slope), len(raw_slope[0])), itemsize=1)
for ind, row in enumerate(raw_slope):
	slope[ind, :] = list(row)

# Part 1
slope_right = 3
slope_down = 1
n_trees = count_trees(slope_right, slope_down)
print(f"Part 1: {n_trees} trees")

# Part 2
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_product = 1
for slope_right, slope_down in slopes:
    n_trees = count_trees(slope_right, slope_down)
    print(f"Slope is {(slope_right, slope_down)}, result is {n_trees}")
    tree_product *= n_trees
print(f"Part 2: result is {tree_product}")

