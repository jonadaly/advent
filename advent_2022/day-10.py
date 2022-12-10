from itertools import product
from pathlib import Path

import numpy as np

instructions: list[str] = Path("day-10-input.txt").read_text().strip().split("\n")

changes: list[int] = [1]
for instruction in instructions:
    changes.append(0)
    if instruction != "noop":
        changes.append(int(instruction.split(" ")[1]))
signal_strengths: np.ndarray = np.cumsum(changes)
total = sum(i * signal_strengths[i - 1] for i in [20, 60, 100, 140, 180, 220])
print(f"Part 1: Total signal strength is {total}")

crt_screen: list[list[str]] = [["."] * 40 for _ in range(6)]

# Fancy double for-loop with enumeration for the cycle number.
for cycle, (i_row, i_col) in enumerate(product(range(6), range(40))):
    sprite = signal_strengths[cycle]
    crt_screen[i_row][i_col] = "#" if i_col in [sprite - 1, sprite, sprite + 1] else "."

print("Part 2:")
print("\n".join("".join(row) for row in crt_screen))
