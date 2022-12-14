import itertools
from pathlib import Path

import numpy as np

CAVERN_HEIGHT = 500
CAVERN_WIDTH = 1000


def print_cavern(cavern: np.ndarray, min_x: int, max_x: int, max_y: int) -> None:
    cavern = np.copy(cavern)
    cavern[0, CAVERN_HEIGHT] = "+"
    trimmed_cavern = cavern[: max_y + 1, min_x : max_x + 1]
    print(f"({min_x})", " " * (trimmed_cavern.shape[1] - 3), f"({max_x})")
    for i_row, row in enumerate(trimmed_cavern):
        print(f"{i_row:03d}", "".join(row))


rock_paths: list[str] = Path("day-14-input.txt").read_text().strip().split("\n")

cavern: np.ndarray = np.full((CAVERN_HEIGHT, CAVERN_WIDTH), ".", dtype=str)
max_ovr_y = 0
min_ovr_x = CAVERN_WIDTH
max_ovr_x = 0
for rock_path in rock_paths:
    nodes = rock_path.split(" -> ")
    for prev, current in zip(nodes, nodes[1:]):
        x_1, y_1 = tuple(map(int, prev.split(",")))
        x_2, y_2 = tuple(map(int, current.split(",")))
        x_min, x_max = sorted((x_1, x_2))
        y_min, y_max = sorted((y_1, y_2))
        cavern[y_min : y_max + 1, x_min : x_max + 1] = "#"
        max_ovr_y = max(max_ovr_y, y_max)
        min_ovr_x = min(min_ovr_x, x_min)
        max_ovr_x = max(max_ovr_x, x_max)


def simulate_scan(
    cavern: np.ndarray,
    min_ovr_x: int,
    max_ovr_x: int,
    max_ovr_y: int,
    allow_past: bool,
    should_print: bool,
) -> int:
    if should_print:
        print("Starting simulation")
        print_cavern(cavern, min_ovr_x, max_ovr_x, max_ovr_y)
    for i_sim in itertools.count(start=1):
        curr_x = CAVERN_HEIGHT
        # Find the deepest empty space
        curr_y = np.argwhere(cavern[:, curr_x] != ".")[0][0] - 1
        if curr_y == -1:
            # Top is blocked
            if should_print:
                print(f"Blocked on {i_sim}")
                print_cavern(cavern, min_ovr_x, max_ovr_x, max_ovr_y)
            return i_sim - 1
        # Trickle the sand!
        while True:
            if allow_past is False and (
                curr_x < min_ovr_x or curr_x > max_ovr_x or curr_y > max_ovr_y
            ):
                if should_print:
                    print(f"shot past on {i_sim}")
                    print_cavern(cavern, min_ovr_x, max_ovr_x, max_ovr_y)
                return i_sim - 1
            if cavern[curr_y + 1, curr_x] == ".":
                curr_y += 1
                continue
            if cavern[curr_y + 1, curr_x - 1] == ".":
                curr_y += 1
                curr_x -= 1
                continue
            if cavern[curr_y + 1, curr_x + 1] == ".":
                curr_y += 1
                curr_x += 1
                continue
            cavern[curr_y, curr_x] = "o"
            break
    return -1  # Can't get here, satisfy mypy


num_blocks_p1 = simulate_scan(
    np.copy(cavern),
    min_ovr_x,
    max_ovr_x,
    max_ovr_y,
    allow_past=False,
    should_print=False,
)
print(f"Part 1: {num_blocks_p1} units of sand have come to rest")


max_ovr_y += 2
cavern[max_ovr_y, :] = "#"
num_blocks_p2 = simulate_scan(
    np.copy(cavern),
    min_ovr_x,
    max_ovr_x,
    max_ovr_y,
    allow_past=True,
    should_print=True,
)
print(f"Part 2: {num_blocks_p2} units of sand have come to rest")
