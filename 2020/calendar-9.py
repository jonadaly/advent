from pathlib import Path
import collections
import itertools
import numpy as np

NUM_PREAMBLE = 25
numbers = list(map(int, Path("9.txt").read_text().strip().split("\n")))

# Part 1
buffer = collections.deque(numbers[:NUM_PREAMBLE])
invalid_number = None
for number in numbers[NUM_PREAMBLE:]:
    if number not in [sum(comb) for comb in itertools.combinations(buffer, 2)]:
        invalid_number = number
        break
    buffer.popleft()
    buffer.append(number)
print(f"Part 1: first invalid number is {invalid_number}")

# Part 2
matching_range = None
cumsum = list(np.cumsum(numbers))
for comb in itertools.combinations(cumsum, 2):
    if abs(comb[0] - comb[1]) == invalid_number:
        idx_start = cumsum.index(comb[0]) + 1
        idx_end = cumsum.index(comb[1])
        if idx_end - idx_start > 1: # Don't allow "contiguous block" of only one number
            matching_range = numbers[idx_start:idx_end+1]
            break
print(f"Part 2: Sum is {min(matching_range) + max(matching_range)}")
