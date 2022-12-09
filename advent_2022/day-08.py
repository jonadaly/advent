import numpy as np


def get_viz(tree, neighbours) -> int:
    if neighbours.size == 0:
        return 0
    if not any(neighbours >= tree):
        return len(neighbours)
    return np.argmax(neighbours >= tree) + 1


grid = np.genfromtxt("day-08-input.txt", delimiter=1, dtype=int)
total = 0
max_scen = 0
for i_row in range(grid.shape[0]):
    for i_col in range(grid.shape[1]):
        tree = grid[i_row, i_col]
        left = grid[i_row, :i_col]
        right = grid[i_row, i_col + 1 :]
        top = grid[:i_row, i_col]
        bottom = grid[i_row + 1 :, i_col]
        # Tree visible if everything between it and the edge is smaller.
        if any(
            [
                np.all(left < tree),
                np.all(right < tree),
                np.all(top < tree),
                np.all(bottom < tree),
            ]
        ):
            total += 1
        # Score is product of visibility in each direction
        product = (
            get_viz(tree, np.flip(left))
            * get_viz(tree, right)
            * get_viz(tree, np.flip(top))
            * get_viz(tree, bottom)
        )
        max_scen = max(max_scen, product)

print(f"Part 1: {total} trees are visible from outside")
print(f"Part 2: {max_scen} trees are visible from best location")
