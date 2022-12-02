import re
from collections import Counter
from pathlib import Path
from typing import Optional

instructions_raw = Path("22.txt").read_text().strip().split("\n")
instructions = []
for instruction_raw in instructions_raw:
    action, *groups = re.match(
        r"^(.+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$",
        instruction_raw,
    ).groups()
    coordinates = tuple(map(int, groups))
    instructions.append((action, coordinates))

# Part 1
part1_cubes_on = set()
for action, coordinates in instructions:
    if any(abs(i) > 50 for i in coordinates):
        break
    x1, x2, y1, y2, z1, z2 = coordinates
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                if action == "on":
                    part1_cubes_on.add((x, y, z))
                else:
                    part1_cubes_on.discard((x, y, z))
print(f"Part 1: {len(part1_cubes_on)} cubes are switched on after initialisation")

# Part 2


def get_overlap(cube1: tuple, cube2: tuple) -> Optional[tuple]:
    """
    Returns the coordinates of overlaps between two cuboids. Coordinates are in the form:
    (x1, x2, y1, y2, z1, z2)
    """
    max_x1 = max(cube1[0], cube2[0])
    min_x2 = min(cube1[1], cube2[1])
    max_y1 = max(cube1[2], cube2[2])
    min_y2 = min(cube1[3], cube2[3])
    max_z1 = max(cube1[4], cube2[4])
    min_z2 = min(cube1[5], cube2[5])
    if max_x1 <= min_x2 and max_y1 <= min_y2 and max_z1 <= min_z2:
        return max_x1, min_x2, max_y1, min_y2, max_z1, min_z2
    return None


all_cubes = Counter()
for action, coordinates in instructions:
    new_cubes = Counter()
    for k, v in all_cubes.items():
        overlap = get_overlap(cube1=coordinates, cube2=k)
        if overlap is not None:
            new_cubes[overlap] -= v
    if action == "on":
        new_cubes[coordinates] += 1
    all_cubes.update(new_cubes)  # The Counter.update() method adds the counts together.

part2_cubes_on = sum(
    v * (k[1] - k[0] + 1) * (k[3] - k[2] + 1) * (k[5] - k[4] + 1)
    for k, v in all_cubes.items()
)
print(f"Part 2: {part2_cubes_on} cubes are switched on after full reboot")
