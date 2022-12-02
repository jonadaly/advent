from collections import Counter
from pathlib import Path

polymer, rules = Path("14.txt").read_text().strip().split("\n\n")
pairs = zip(polymer.strip(), polymer.strip()[1:])
pair_counter = Counter(("".join(p) for p in pairs))
letter_counter = Counter(c for c in polymer.strip())
for i in range(40):
    pair_counter_increment = Counter()
    for rule in rules.strip().split("\n"):
        pair, to_add = rule.split(" -> ")
        n_existing = pair_counter[pair]
        pair_counter_increment[pair[0] + to_add] += n_existing
        pair_counter_increment[to_add + pair[1]] += n_existing
        pair_counter_increment[pair] -= n_existing
        letter_counter[to_add] += n_existing
    pair_counter = pair_counter + pair_counter_increment
    diff = letter_counter.most_common()[0][1] - letter_counter.most_common()[-1][1]
    if i == 9:
        print(f"Part 1: After 10 iterations diff is {diff}")
    if i == 39:
        print(f"Part 2: After 40 iterations diff is {diff}")
