from itertools import product
from pathlib import Path

import numpy as np

CYCLES = (20, 60, 100, 140, 180, 220)
WIDTH = 40
HEIGHT = 6

instructions: list[str] = Path("day-10-input.txt").read_text().strip().split("\n")

changes: list[int] = [1]
for instruction in instructions:
    changes.append(0)
    if instruction != "noop":
        changes.append(int(instruction.split(" ")[1]))
signal_strengths: np.ndarray = np.cumsum(changes)
total = sum(i * signal_strengths[i - 1] for i in CYCLES)
print(f"Part 1: Total signal strength is {total}")

# Build screen repr.
screen: list[list[str]] = [["."] * WIDTH for _ in range(HEIGHT)]

# Fancy double for-loop with enumeration for the cycle number.
for cycle, (i_row, i_col) in enumerate(product(range(HEIGHT), range(WIDTH))):
    pos = signal_strengths[cycle]
    screen[i_row][i_col] = "#" if i_col in [pos - 1, pos, pos + 1] else "."

print("Part 2:")
print("\n".join("".join(row) for row in screen))
