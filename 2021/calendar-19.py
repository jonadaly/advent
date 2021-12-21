import itertools
import math
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict

import numpy as np

scanners_raw = Path("19.txt").read_text().strip().split("\n\n")

# Create the 24 possible rotation matrices.
# https://www.andre-gaschler.com/rotationconverter/
rotate_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
rotate_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
rotate_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
rotations = []
rotations_str = []
for i in range(4):
    rot1 = np.linalg.matrix_power(rotate_x, i)
    for j in range(4):
        rot2 = np.linalg.matrix_power(rotate_y, j)
        for k in range(4):
            rot3 = np.linalg.matrix_power(rotate_z, k)
            ovr_rot = rot1 @ rot2 @ rot3
            if str(ovr_rot) not in rotations_str:
                # (yes this is dumb but 3D rotations are confusing)
                rotations.append(ovr_rot)
                rotations_str.append(str(ovr_rot))

# Build the scanners.
scanners = []
for scanner_raw in scanners_raw:
    distances = []
    fingerprints: Dict[tuple, list] = defaultdict(list)
    raw_header, *raw_coord_lines = scanner_raw.split("\n")
    scanner_id = int(re.match(r"^--- scanner (\d+) ---$", raw_header).groups()[0])
    coordinates = [tuple(map(int, r.split(","))) for r in raw_coord_lines]
    for c1, c2 in itertools.combinations(raw_coord_lines, r=2):
        if c1 == c2:
            continue
        x1, y1, z1 = tuple(map(int, c1.split(",")))
        x2, y2, z2 = tuple(map(int, c2.split(",")))
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        distances.append(distance)
        fingerprints[(x1, y1, z1)].append(distance)
        fingerprints[(x2, y2, z2)].append(distance)
    scanners.append(
        {
            "id": scanner_id,
            "distances": distances,
            "coordinates": coordinates,
            "fingerprints": fingerprints,
        }
    )

scanners[0]["scanner_location"] = (0, 0, 0)
aligned = [scanners[0]]
remaining = deque(scanners[1:])
while remaining:
    scanner_to_align = remaining.popleft()
    match_found = False
    for a in aligned:
        in_common = set(a["distances"]) & set(scanner_to_align["distances"])
        if len(in_common) >= math.comb(12, 2):
            # Found a match.
            match_found = True

            # alignment
            matched_points = []
            for p1 in scanner_to_align["coordinates"]:
                distances = scanner_to_align["fingerprints"][p1]
                for p2 in a["coordinates"]:
                    if len(set(distances) & set(a["fingerprints"][p2])) >= 11:
                        matched_points.append((p1, p2))
            assert len(matched_points) >= 12

            # y = ax + b (a is the rotation matrix, b is the translation matrix)
            x = np.array([i[0] for i in matched_points])
            y = np.array([i[1] for i in matched_points])
            correct_rotation = None
            offset = None
            for rot in rotations:
                transformed = np.subtract(y, x @ rot)
                if len(set(transformed.flatten())) <= 3:
                    # found the matching rotation.
                    correct_rotation = rot
                    offset = transformed[0]
                    break

            coordinates_lookup = {
                p: tuple(np.add(offset, p @ correct_rotation))
                for p in scanner_to_align["coordinates"]
            }

            aligned_scanner = {
                "id": scanner_to_align["id"],
                "distances": scanner_to_align["distances"],
                "coordinates": [
                    coordinates_lookup[c] for c in scanner_to_align["coordinates"]
                ],
                "fingerprints": {
                    coordinates_lookup[k]: v
                    for k, v in scanner_to_align["fingerprints"].items()
                },
                "scanner_location": offset,
            }

            aligned.append(aligned_scanner)
            # print(f'Scanner {aligned_scanner["id"]} at {aligned_scanner["scanner_location"]}')
            break

    if not match_found:
        # print(f"No match found for scanner {scanner_to_align['id']}")
        remaining.append(scanner_to_align)

all_beacons = set().union(*[s["coordinates"] for s in aligned])
print(f"Part 1: there are {len(all_beacons)} beacons in total")

scanner_locations = [s["scanner_location"] for s in aligned]
max_manhattan = 0
for b1, b2 in itertools.combinations(scanner_locations, r=2):
    manhattan_distance = abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])
    max_manhattan = max(max_manhattan, manhattan_distance)
print(f"Part 2: max distance between scanners is {max_manhattan}")
