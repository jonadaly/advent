from collections import Counter
from pathlib import Path

raw_input = Path("01.txt").read_text().strip().split("\n")
left = sorted([int(x.split()[0]) for x in raw_input])
right = sorted([int(x.split()[1]) for x in raw_input])
total = sum([abs(a - b) for a, b in zip(left, right)])
print(f"Part 1: total distance is {total}")

count_right = Counter(right)
similarity_score = sum(x * count_right[x] for x in left)
print(f"Part 2: similarity score is {similarity_score}")
