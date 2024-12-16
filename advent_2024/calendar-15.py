from pathlib import Path
import numpy as np

raw_map, raw_movements = Path("15.txt").read_text().strip().split("\n\n")
original_map = np.array([list(line) for line in raw_map.split("\n")], dtype=str)
movements = "".join(raw_movements.split())

map_dir = {">": 1j, "<": -1j, "v": 1, "^": -1}


def get_touching_box_coords(
    current: complex, direction: complex, map: np.ndarray
) -> set[complex] | None:
    boxes = set()
    while True:
        current += direction
        current_val = map[int(current.real)][int(current.imag)]
        if current_val == "O":
            boxes.add(current)
        if current_val == "[":
            boxes.add(current)
            if direction.imag == 0:
                upstream_boxes = get_touching_box_coords(current + 1j, direction, map)
                if upstream_boxes is None:
                    return None
                boxes |= upstream_boxes
        if current_val == "]":
            boxes.add(current - 1j)
            if direction.imag == 0:
                upstream_boxes = get_touching_box_coords(current - 1j, direction, map)
                if upstream_boxes is None:
                    return None
                boxes |= upstream_boxes
        if current_val == "#":
            return None
        if current_val == ".":
            return boxes


## Part 2: original map
map_part1 = original_map.copy()
current = np.where(map_part1 == "@")[0][0] + np.where(map_part1 == "@")[1][0] * 1j
for movement in movements:
    direction = map_dir[movement]
    goal = current + direction
    boxes = get_touching_box_coords(current, direction, map_part1)
    if boxes is None:
        continue
    for box in boxes:
        shifted = box + direction
        map_part1[int(shifted.real)][int(shifted.imag)] = "O"
    map_part1[int(current.real)][int(current.imag)] = "."
    map_part1[int(goal.real)][int(goal.imag)] = "@"
    current = goal

gps_sum = (
    np.where(map_part1 == "O")[0].sum() * 100 + np.where(map_part1 == "O")[1].sum()
)
print(f"Part 1: GPS sum is {gps_sum}")

## Part 2: wider map
map_part2_1 = original_map.copy()
map_part2_1[map_part2_1 == "O"] = "["
map_part2_2 = original_map.copy()
map_part2_2[map_part2_2 == "O"] = "]"
map_part2_2[map_part2_2 == "@"] = "."
map_part2 = np.empty(
    (map_part2_1.shape[0], map_part2_1.shape[1] + map_part2_2.shape[1]), dtype=str
)
map_part2[:, ::2] = map_part2_1
map_part2[:, 1::2] = map_part2_2

current = np.where(map_part2 == "@")[0][0] + np.where(map_part2 == "@")[1][0] * 1j
for movement in movements:
    direction = map_dir[movement]
    goal = current + direction
    boxes = get_touching_box_coords(current, direction, map_part2)
    if boxes is None:
        continue
    for box in boxes:
        map_part2[int(box.real)][int(box.imag)] = "."
        map_part2[int(box.real)][int(box.imag) + 1] = "."
    for box in boxes:
        shifted = box + direction
        map_part2[int(shifted.real)][int(shifted.imag)] = "["
        map_part2[int(shifted.real)][int(shifted.imag) + 1] = "]"
    map_part2[int(current.real)][int(current.imag)] = "."
    map_part2[int(goal.real)][int(goal.imag)] = "@"
    current = goal


gps_sum = (
    np.where(map_part2 == "[")[0].sum() * 100 + np.where(map_part2 == "[")[1].sum()
)
print(f"Part 2: GPS sum is {gps_sum}")
