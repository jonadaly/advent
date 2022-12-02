from pathlib import Path

import numpy as np
from numpy.lib import stride_tricks

enhance_algo, input_image_raw = Path("20.txt").read_text().strip().split("\n\n")
input_image_raw_lines = input_image_raw.split("\n")
height = len(input_image_raw_lines)
width = len(input_image_raw_lines[0])
working_image = np.ndarray((height, width)).astype(int)
for ind, row in enumerate(input_image_raw_lines):
    working_image[ind, :] = [1 if r == "#" else 0 for r in row]

np.set_printoptions(edgeitems=6)
to_pad = 0
for i in range(50):
    # Pad image with whatever the outer pixels are.
    padded_image = np.pad(
        working_image, [(3, 3), (3, 3)], mode="constant", constant_values=to_pad
    )
    windows = stride_tricks.sliding_window_view(padded_image, (3, 3))
    new_image = padded_image.copy()
    for i_row, row in enumerate(padded_image):
        if i_row == 0 or i_row == padded_image.shape[0] - 1:
            continue
        for i_col, element in enumerate(row):
            if i_col == 0 or i_col == padded_image.shape[1] - 1:
                continue
            # Get binary representation of 3x3 window.
            bin_str = "".join(map(str, windows[i_row - 1, i_col - 1].flatten()))
            # Set the new pixel value using a lookup.
            new_image[i_row, i_col] = 1 if enhance_algo[int(bin_str, 2)] == "#" else 0
    # Trim the image to get rid of unnecessary rows.
    working_image = new_image[2:-2, 2:-2]
    # Set the value to pad with next time.
    key_idx = enhance_algo[0] if to_pad == 0 else enhance_algo[-1]
    to_pad = 1 if key_idx == "#" else 0
    # print(i, working_image)
    if i == 1:
        print(f"Part 1: {working_image.sum()} lit pixels after 2 iterations")
    if i == 49:
        print(f"Part 2: {working_image.sum()} lit pixels after 50 iterations")
