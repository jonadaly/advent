from pathlib import Path
import numpy as np
from typing import Dict, Tuple, List


def print_slice(cubes, idepth, itime):
    print(f"z={idepth}, t={itime}")
    for i in range(
        min(k[0] for k in cubes.keys()), max(k[0] for k in cubes.keys()) + 1
    ):
        for j in range(
            min(k[1] for k in cubes.keys()), max(k[1] for k in cubes.keys()) + 1
        ):
            print("#" if cubes[i, j, idepth, itime] else ".", end="")
        print("")


lines = Path("17.txt").read_text().strip().split("\n")

cubes: Dict[Tuple[int, int, int, int], bool] = {}
for irow, row in enumerate(lines):
    for icol, char in enumerate(row):
        cubes[(irow, icol, 0, 0)] = char == "#"

# print_slice(cubes, 0, 0)

# Part 1
# NEARBY: List[Tuple[int, int, int]] = []
# for i in [-1, 0, 1]:
#     for j in [-1, 0, 1]:
#         for k in [-1, 0, 1]:
#             NEARBY.append((i, j, k))
# NEARBY.remove((0, 0, 0))
# for t in range(1, 7):
#     new_cubes = {**cubes}
#     # print(cubes)
#     # print(new_cubes)
#     # print(f"z range: {list(range(min(k[2] for k in cubes.keys()) - 1, max(k[2] for k in cubes.keys())+2))}")
#     for z in range(
#         min(k[2] for k in cubes.keys()) - 1, max(k[2] for k in cubes.keys()) + 2
#     ):
#         # print(f"i range: {list(range(min(k[0] for k in cubes.keys()) - 1, max(k[0] for k in cubes.keys())+2))}")
#         for i in range(
#             min(k[0] for k in cubes.keys()) - 1, max(k[0] for k in cubes.keys()) + 2
#         ):
#             # print(f"j range: {list(range(min(k[1] for k in cubes.keys()) - 1, max(k[1] for k in cubes.keys())+2))}")
#             for j in range(
#                 min(k[1] for k in cubes.keys()) - 1, max(k[1] for k in cubes.keys()) + 2
#             ):
#                 old_active = cubes.get((i, j, z, t - 1), False)
#                 new_active = False
#                 total = 0
#                 for i2, j2, k2 in NEARBY:
#                     # print(f"offset: {(i2, j2, k2)}")
#                     # print(f"Trying {(i + i2, j + j2, z + k2, t-1)}: which is {cubes.get((i + i2, j + j2, z + k2, t-1), False)}")
#                     if cubes.get((i + i2, j + j2, z + k2, t - 1), False):
#                         total += 1
#                 # print(f"{(i, j, z, t)}: total is {total}")
#                 if old_active and total in (2, 3):
#                     new_active = True
#                 if not old_active and total == 3:
#                     new_active = True
#                 new_cubes[(i, j, z, t)] = new_active
#         # print_slice(new_cubes, z, t)
#     cubes = new_cubes
# n_active = sum([v for k, v in cubes.items() if k[3] == 6])
# print(f"Part 1: {n_active} cubes are active")

# Part 2
NEARBY: List[Tuple[int, int, int, int]] = []
for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            for t in [-1, 0, 1]:
                NEARBY.append((i, j, k, t))
NEARBY.remove((0, 0, 0, 0))
for gen in range(1, 7):
    new_cubes = {**cubes}
    for i in range(
        min(k[0] for k in cubes.keys()) - 1, max(k[0] for k in cubes.keys()) + 2
    ):
        for j in range(
            min(k[1] for k in cubes.keys()) - 1, max(k[1] for k in cubes.keys()) + 2
        ):
            for z in range(
                min(k[2] for k in cubes.keys()) - 1, max(k[2] for k in cubes.keys()) + 2
            ):
                for t in range(
                    min(k[3] for k in cubes.keys()) - 1, max(k[3] for k in cubes.keys()) + 2
                ):
                    old_active = cubes.get((i, j, z, t), False)
                    new_active = False
                    total = 0
                    for i2, j2, k2, t2 in NEARBY:
                        # print(f"offset: {(i2, j2, k2)}")
                        # print(f"Trying {(i + i2, j + j2, z + k2, t-1)}: which is {cubes.get((i + i2, j + j2, z + k2, t-1), False)}")
                        if cubes.get((i + i2, j + j2, z + k2, t + t2), False):
                            total += 1
                    # print(f"{(i, j, z, t)}: total is {total}")
                    if old_active and total in (2, 3):
                        new_active = True
                    if not old_active and total == 3:
                        new_active = True
                    new_cubes[(i, j, z, t)] = new_active
            # print_slice(new_cubes, z, t)
    cubes = new_cubes
    print(f"Done gen {gen}")
print(f"Part 2: {sum(cubes.values())} cubes are active")
