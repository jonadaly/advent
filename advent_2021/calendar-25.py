from pathlib import Path

import numpy as np


def print_area(_area):
    temp_cav = np.copy(_area)
    for row in temp_cav:
        print(row.tostring().decode("utf8"))
    print("\n")


raw_area = Path("25.txt").read_text().strip().split("\n")
height = len(raw_area)
width = len(raw_area[0])
area = np.chararray((height, width))
for ind, row in enumerate(raw_area):
    area[ind, :] = list(row)


def move(_area):
    right_pointing = _area == b">"
    can_move_right = np.logical_and(
        right_pointing, np.concatenate([_area[:, 1:], _area[:, :1]], axis=1) == b"."
    )
    can_move_right_src = np.where(can_move_right)
    can_move_right_dst = (
        can_move_right_src[0],
        np.array([(t + 1) % width for t in can_move_right_src[1]], dtype="int64"),
    )
    _area[can_move_right_src] = b"."
    _area[can_move_right_dst] = b">"

    down_pointing = _area == b"v"
    can_move_down = np.logical_and(
        down_pointing, np.concatenate([_area[1:, :], _area[:1, :]], axis=0) == b"."
    )
    can_move_down_src = np.where(can_move_down)
    can_move_down_dst = (
        np.array([(t + 1) % height for t in can_move_down_src[0]], dtype="int64"),
        can_move_down_src[1],
    )
    _area[can_move_down_src] = b"."
    _area[can_move_down_dst] = b"v"


i = 1
while True:
    old_area = area.copy()
    move(area)
    # print(f"Step {i}")
    # print_area(area)
    if np.char.compare_chararrays(old_area, area, "==", True).all():
        break
    i += 1

print(f"Part 1: creatures stop moving after {i} steps")
