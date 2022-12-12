import math
import string
from itertools import product
from typing import Optional

import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.core.heuristic import null
from pathfinding.core.node import Node
from pathfinding.finder.a_star import MAX_RUNS, TIME_LIMIT, AStarFinder

HEIGHTS = {v: k for k, v in enumerate(string.ascii_lowercase)}

TERRAIN = np.genfromtxt("day-12-input.txt", delimiter=1, dtype=str)
start: tuple[int, int] = tuple(np.argwhere(TERRAIN == "S")[0])  # type: ignore
finish: tuple[int, int] = tuple(np.argwhere(TERRAIN == "E")[0])  # type: ignore
TERRAIN[TERRAIN == "S"] = "a"
TERRAIN[TERRAIN == "E"] = "z"


class CustomFinder(AStarFinder):
    counter = 0

    def __init__(self):
        super().__init__(
            heuristic=null,
            weight=1,
            diagonal_movement=DiagonalMovement.never,
            time_limit=TIME_LIMIT,
            max_runs=MAX_RUNS,
        )

    # Just override this bit.
    def find_neighbors(
        self,
        grid: Grid,
        node: Node,
        diagonal_movement: Optional[DiagonalMovement] = None,
    ) -> list[Node]:
        return [
            node_b
            for node_b in grid.neighbors(node, diagonal_movement=diagonal_movement)
            if HEIGHTS[TERRAIN[node_b.y, node_b.x]] - HEIGHTS[TERRAIN[node.y, node.x]]
            <= 1
        ]


def do_it(start: tuple[int, int], finish: tuple[int, int]) -> int:
    grid = Grid(matrix=np.ones(TERRAIN.shape))
    path, _ = CustomFinder().find_path(
        grid.node(start[1], start[0]), grid.node(finish[1], finish[0]), grid
    )
    return len(path) - 1


print(f"Part 1: took {do_it(start, finish)} steps from {start} to {finish}")

# Part 2 takes about 10 seconds.
min_steps = math.inf
for (i, j) in product(range(TERRAIN.shape[0]), range(TERRAIN.shape[1])):
    if TERRAIN[i, j] != "a":
        continue  # Not a start point
    steps = do_it((i, j), finish)
    if steps == -1:
        continue  # no path
    min_steps = min(min_steps, steps)
print(f"Part 2: took {min_steps} steps to get to closest valid starting point")
