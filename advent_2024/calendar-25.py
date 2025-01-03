from itertools import product
from pathlib import Path


raw_locks_and_keys = Path("25.txt").read_text().strip().split("\n\n")

keys = []
locks = []
for raw_lock_or_key in raw_locks_and_keys:
    lines = raw_lock_or_key.split("\n")
    totals = [
        sum(1 for line in lines if line[i] == "#") - 1 for i in range(len(lines[0]))
    ]
    if all(l == "." for l in lines[0]):
        keys.append(totals)
    else:
        locks.append(totals)

fits = sum(1 for pair in product(locks, keys) if all(l + k <= 5 for l, k in zip(*pair)))
print(f"Part 1: there are {fits} ways to fit a key into a lock")
