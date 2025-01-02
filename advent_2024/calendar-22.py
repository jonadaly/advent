from collections import defaultdict, deque
from pathlib import Path


numbers = Path("22.txt").read_text().strip().split("\n")


def mix(number1: int, number2: int) -> int:
    return number1 ^ number2


def prune(number1: int) -> int:
    return number1 % 16777216


def evolve(before: int) -> int:
    step1 = prune(mix(before, before * 64))
    step2 = prune(mix(step1, step1 // 32))
    return prune(mix(step2, step2 * 2048))


total = 0
all_sequences = {}
for num_str in numbers:
    number = int(num_str)
    digits = deque([number % 10], maxlen=5)
    sequences = {}
    for i in range(2000):
        number = evolve(number)
        digits.append(number % 10)
        if len(digits) > 4:
            this_sequence = (
                digits[-4] - digits[-5],
                digits[-3] - digits[-4],
                digits[-2] - digits[-3],
                digits[-1] - digits[-2],
            )
            if this_sequence not in sequences:
                sequences[this_sequence] = number % 10
    all_sequences[number] = sequences
    total += number
print(f"Part 1: total is {total}")

scores: dict[tuple, int] = defaultdict(int)
for sequences in all_sequences.values():
    for sequence, bananas in sequences.items():
        scores[sequence] = scores[sequence] + bananas
max_score = max(scores.values())
print(f"Part 2: max score is {max_score}")
