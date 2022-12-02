from pathlib import Path

import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder


def calculate_path_cost(area):
    grid = Grid(matrix=area)
    start = grid.node(0, 0)
    end = grid.node(area.shape[0] - 1, area.shape[1] - 1)
    finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)
    # print(grid.grid_str(path=path, start=start, end=end))
    return sum(area[p[1], p[0]] for p in path[1:])


raw_area = Path("15.txt").read_text().strip().split("\n")
height = len(raw_area)
width = len(raw_area[0])
first_area = np.ndarray((height, width))
for ind, row in enumerate(raw_area):
    first_area[ind, :] = list(row)

# Tile the area 5x5 for part 2 (with annoying maths because 9 wraps back around to 1 instead of 0).
tiled_area = np.ndarray((height * 5, width * 5))
for i_row in range(5):
    for i_col in range(5):
        tiled_area[
            i_row * height : (i_row + 1) * height, i_col * width : (i_col + 1) * width
        ] = (np.mod(first_area + i_row + i_col - 1, 9) + 1)

path_cost_part1 = calculate_path_cost(first_area)
print(f"Part 1: path cost is {path_cost_part1}")
print("Starting part 2 (can take >30s)")
path_cost_part2 = calculate_path_cost(tiled_area)
print(f"Part 2: path cost is {path_cost_part2}")
