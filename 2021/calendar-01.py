from pathlib import Path

import numpy as np

raw_depths = Path("01.txt").read_text().strip().split("\n")
depths = list(map(int, raw_depths))

diffs = np.diff(depths)
n_positive = len([d for d in diffs if d > 0])
print(f"Part 1: depth increases {n_positive} times")

windowed = np.convolve(depths, np.ones(3), "valid")
diffs_windowed = np.diff(windowed)
n_positive_windowed = len([d for d in diffs_windowed if d > 0])
print(f"Part 2: depth increases {n_positive_windowed} times")
