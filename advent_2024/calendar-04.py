from pathlib import Path
import re
import numpy as np

raw_input = Path("04.txt").read_text().strip().split("\n")
grid = np.array([list(line) for line in raw_input], dtype=str)

# Part 1 - Word-search for "XMAS". There's a more efficient way (scan for matching tiles), but that's boring.
grid_rotated = grid[::-1].T
grid_diagonals = [
    np.diagonal(grid[i:, :], axis1=0, axis2=1)
    for i in reversed(range(1, grid.shape[0]))
] + [np.diagonal(grid[:, i:], axis1=0, axis2=1) for i in range(0, grid.shape[0])]
grid_diagonals_other = [
    np.diagonal(grid_rotated[i:, :], axis1=0, axis2=1)
    for i in reversed(range(1, grid_rotated.shape[0]))
] + [
    np.diagonal(grid_rotated[:, i:], axis1=0, axis2=1)
    for i in range(0, grid_rotated.shape[0])
]
dir1 = ["".join(r) for r in grid]
dir2 = ["".join(r) for r in grid_rotated]
dir3 = ["".join(r) for r in grid[:, ::-1]]
dir4 = ["".join(r) for r in grid_rotated[:, ::-1]]
dir5 = ["".join(r) for r in grid_diagonals]
dir6 = ["".join(r[::-1]) for r in dir5]
dir7 = ["".join(r) for r in grid_diagonals_other]
dir8 = ["".join(r[::-1]) for r in dir7]
xmas_count = sum(
    len(re.findall(r"XMAS", s))
    for s in dir1 + dir2 + dir3 + dir4 + dir5 + dir6 + dir7 + dir8
)
print(f"Part 1: XMAS count is {xmas_count}")

# Part 2 - switch to tiling because we have to now.
base_tile = np.array(
    [
        ["M", ".", "S"],
        [".", "A", "."],
        ["M", ".", "S"],
    ]
)
tiles = [np.rot90(base_tile, i) for i in range(4)]
mask = base_tile == "."

total = 0
for i in range(grid.shape[0] - 2):
    for j in range(grid.shape[1] - 2):
        window = grid[i : i + 3, j : j + 3].copy()
        window[mask] = "."
        if any(np.array_equal(window, t) for t in tiles):
            total += 1

print(f"Part 2: X-MAS count is {total}")
