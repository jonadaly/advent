import itertools
import math
import re
from collections import deque, defaultdict
from pathlib import Path
from typing import Dict, List

import numpy as np
from numpy import ndarray

scanners_raw = Path("19-example.txt").read_text().strip().split("\n\n")

# https://www.andre-gaschler.com/rotationconverter/
rotate_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
rotate_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
rotate_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

# Generate 24 rotations
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

scanners = []
for scanner_raw in scanners_raw:
    pairs = {}
    point_fingerprints: Dict[tuple, list] = defaultdict(list)
    raw_header, *raw_coord_lines = scanner_raw.split("\n")
    scanner_id = int(re.match(r"^--- scanner (\d+) ---$", raw_header).groups()[0])
    coordinates = [tuple(map(int, r.split(","))) for r in raw_coord_lines]
    for c1, c2 in itertools.combinations(raw_coord_lines, r=2):
        if c1 == c2:
            continue
        x1, y1, z1 = tuple(map(int, c1.split(",")))
        x2, y2, z2 = tuple(map(int, c2.split(",")))
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        pairs[((x1, y1, z1), (x2, y2, z2))] = distance
        point_fingerprints[(x1, y1, z1)].append(distance)
        point_fingerprints[(x2, y2, z2)].append(distance)
    scanners.append({"id": scanner_id, "pairs": pairs, "raw_coordinates": coordinates, "point_fingerprints": point_fingerprints})

scanners[0]["aligned_coordinates"] = scanners[0]["raw_coordinates"].copy()
scanners[0]["aligned_point_fingerprints"] = scanners[0]["point_fingerprints"].copy()
aligned = [scanners[0]]
remaining = deque(scanners[1:])
while remaining:
    print("iterating")
    scanner_to_align = remaining.popleft()
    match_found = False
    for a in aligned:
        in_common = set(a["pairs"].values()) & set(scanner_to_align["pairs"].values())
        if len(in_common) >= math.comb(12, 2):
            # Found a match.
            match_found = True
            print(f"match found between scanner {scanner_to_align['id']} and {a['id']}")

            # alignment
            matched_points = []
            for p1 in scanner_to_align["raw_coordinates"]:
                distances = scanner_to_align['point_fingerprints'][p1]
                for p2 in a["aligned_coordinates"]:
                    # print(len(set(distances) & set(a["point_fingerprints"][p2])))
                    if len(set(distances) & set(a["aligned_point_fingerprints"][p2])) >= 11:
                        print(f"MATCH: {p1} and {p2}")
                        matched_points.append((p1, p2))
            print(len(matched_points))
            assert len(matched_points) >= 12

            # y = ax + b (a is the rotation matrix, b is the translation matrix)
            x = np.array([i[0] for i in matched_points])
            y = np.array([i[1] for i in matched_points])
            correct_rotation = None
            offset = None
            for i, rot in enumerate(rotations):
                # print(i)
                # print(x)
                # print(rot)
                # print("AFTER")
                # print(x@rot)
                # print((x@rot).flatten())
                transformed = np.subtract(y, x@rot)
                print(len(set(transformed.flatten())))
                if len(set(transformed.flatten())) <= 3:
                    # found the matching rotation.
                    correct_rotation = rot
                    offset = transformed[0]

            # p = scanner_to_align["raw_coordinates"][0]
            # print(p)
            # t = np.subtract(offset, p @ correct_rotation)
            # print(t)
            # exit()

            coordinates_lookup = {
                p: tuple(np.subtract(offset, p@correct_rotation)) for p in scanner_to_align["raw_coordinates"]
            }

            aligned_scanner = {
                "id": scanner_to_align["id"],
                "pairs": scanner_to_align["pairs"],
                "raw_coordinates": scanner_to_align["raw_coordinates"],
                "aligned_coordinates": [coordinates_lookup[c] for c in scanner_to_align["raw_coordinates"]],
                "aligned_pairs": {(coordinates_lookup[k[0]], coordinates_lookup[k[1]]): v for k, v in
                          scanner_to_align["pairs"].items()},
                "aligned_point_fingerprints": {coordinates_lookup[k]:v for k, v in scanner_to_align["point_fingerprints"].items()},
                "point_fingerprints": scanner_to_align["point_fingerprints"],
                "scanner_location": offset
            }

            aligned.append(aligned_scanner)
            # print(aligned_scanner["raw_coordinates"])
            # print(aligned_scanner["scanner_location"])

            break
    if not match_found:
        print(f"No match found for scanner {scanner_to_align['id']}")
        remaining.append(scanner_to_align)




