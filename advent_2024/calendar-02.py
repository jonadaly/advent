from pathlib import Path

import numpy as np


raw_input = Path("02.txt").read_text().strip().split("\n")
reports = [list(map(int, r.split())) for r in raw_input]


def is_safe(report: list[int]) -> bool:
    diffs = np.diff(report)
    is_safe_1 = all(diffs > 0) or all(diffs < 0)
    is_safe_2 = all(np.abs(diffs) >= 1) and all(np.abs(diffs) <= 3)
    return is_safe_1 and is_safe_2


def is_safe_with_dampener(report: list[int]) -> bool:
    for i in range(len(report)):
        this_report = report.copy()
        this_report.pop(i)
        if is_safe(this_report):
            return True
    return False


number_safe = sum(is_safe(report) for report in reports)
number_safe_with_dampener = sum(is_safe_with_dampener(report) for report in reports)
print(f"Part 1: {number_safe} reports are safe")
print(f"Part 2: {number_safe_with_dampener} reports are safe with dampener")
