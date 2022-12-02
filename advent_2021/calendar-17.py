import re
from pathlib import Path
from typing import Tuple

target_area_raw = Path("17.txt").read_text().strip()

match = re.match(
    r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$", target_area_raw
)
target_x_min, target_x_max, target_y_min, target_y_max = (
    int(g) for g in match.groups()
)


def run_simulation(_x_dot: int, _y_dot: int) -> Tuple[bool, int]:
    x = 0
    y = 0
    _max_y = 0
    while True:
        x += _x_dot
        y += _y_dot
        _x_dot -= (_x_dot > 0) - (_x_dot < 0)
        _y_dot -= 1
        _max_y = max(_max_y, y)
        if target_x_min <= x <= target_x_max and target_y_min <= y <= target_y_max:
            # Hit!
            return True, _max_y
        if y < target_y_min:
            # Overshot - bail out.
            return False, _max_y


# This is slow, but it's simple and it works.
hit_count = 0
trick_shot_height = 0
# Arbitrarily picked 500 as the range because... it works.
for y_dot in range(-500, 500):
    for x_dot in range(500):
        is_hit, max_y = run_simulation(x_dot, y_dot)
        if is_hit:
            # print(f"x_dot {x_dot}, y_dot {y_dot}: hit with max height {max_y}")
            trick_shot_height = max(trick_shot_height, max_y)
            hit_count += 1
print(f"Part 1: trick shot max height is {trick_shot_height}")
print(f"Part 2: hit count is {hit_count}")
