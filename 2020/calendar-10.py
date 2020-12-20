from pathlib import Path
import numpy as np

adapters = list(map(int, Path("10.txt").read_text().strip().split("\n")))
adapters.sort()

adapters = [0, *adapters, max(adapters)+3]
differences = np.diff(adapters)

# Part 1
number_of_ones = sum(1 for d in differences if d == 1)
number_of_threes = sum(1 for d in differences if d == 3)
print(f"Part 1: Product is {number_of_ones*number_of_threes}")

ways = [1, *np.zeros(adapters[-1])]
for a in adapters[1:]:
    ways[a] = ways[a-1] + ways[a-2] + ways[a-3]
print(f"Part 2: There are {ways[-1]} ways")
