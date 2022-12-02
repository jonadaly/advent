from pathlib import Path

import numpy as np

coords_raw, folds = Path("13.txt").read_text().strip().split("\n\n")

coords = []
for coord in coords_raw.strip().split("\n"):
    x, y = coord.strip().split(",")
    coords.append((int(x), int(y)))

dots = np.zeros((max(c[1] for c in coords) + 1, max(c[0] for c in coords) + 1))
for coord in coords:
    dots[coord[1], coord[0]] = 1

for i, fold in enumerate(folds.strip().split("\n")):
    instruction = fold.strip().split()[-1]
    axis, value = instruction.split("=")
    if axis == "x":
        left_fold = dots[:, : int(value)]
        right_fold = dots[:, int(value) + 1 :]
        height = max(left_fold.shape[0], right_fold.shape[0])
        diff = left_fold.shape[1] - right_fold.shape[1]
        if diff > 0:
            right_fold = np.concatenate(
                [
                    right_fold,
                    np.zeros((height, diff)),
                ],
                axis=1,
            )
        elif diff < 0:
            left_fold = np.concatenate(
                [
                    np.zeros((height, -diff)),
                    left_fold,
                ],
                axis=1,
            )
        dots = left_fold + np.fliplr(right_fold)
    if axis == "y":
        above_fold = dots[: int(value), :]
        below_fold = dots[int(value) + 1 :, :]
        width = max(above_fold.shape[1], below_fold.shape[1])
        diff = above_fold.shape[0] - below_fold.shape[0]
        if diff > 0:
            below_fold = np.concatenate(
                [
                    below_fold,
                    np.zeros((diff, width)),
                ],
                axis=0,
            )
        elif diff < 0:
            above_fold = np.concatenate(
                [
                    np.zeros((-diff, width)),
                    above_fold,
                ],
                axis=0,
            )
        dots = above_fold + np.flipud(below_fold)
    if i == 0:
        print(f"Part 1: {np.count_nonzero(dots)} visible dots after one fold")

result = "\n".join(
    [row.tobytes().decode("utf8") for row in np.where(dots > 0, "#", " ")]
)
print(f"Part 2: Result is\n{result}")
