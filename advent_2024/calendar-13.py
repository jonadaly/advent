import numpy as np
from pathlib import Path
import re

raw_machines = Path("13.txt").read_text().strip().split("\n\n")

total_score = 0
total_score_p2 = 0
for raw_machine in raw_machines:
    raw_match = re.match(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
        raw_machine,
    )
    a1, a3, a2, a4, b1, b2 = map(int, raw_match.groups())  # type: ignore
    A = np.array([[a1, a2], [a3, a4]])
    B = np.array([b1, b2])
    x1, x2 = np.linalg.solve(A, B)
    X1, X2 = np.linalg.solve(A, B + 1e13)
    if round(x1) * a1 + round(x2) * a2 == b1 and round(x1) * a3 + round(x2) * a4 == b2:
        total_score += int(x1 * 3 + x2)
    if (
        round(X1) * a1 + round(X2) * a2 == b1 + 1e13
        and round(X1) * a3 + round(X2) * a4 == b2 + 1e13
    ):
        total_score_p2 += int(X1 * 3 + X2)


print(f"Part 1: total score is {total_score}")
print(f"Part 2: total score is {total_score_p2}")
