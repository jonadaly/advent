from collections import deque
from typing import Dict

# raw_cups = "389125467" # example
raw_cups = "463528179"  # real

# Part 1
N_TURNS = 100
cups = deque([int(c) for c in raw_cups])
for i in range(1, N_TURNS + 1):
    # print(f"-- move {i} --")
    # print(f"cups: {list(cups)}")
    cups.rotate(-1)
    target1 = cups.popleft()
    target2 = cups.popleft()
    target3 = cups.popleft()
    # print(f"pick up: {result1}, {result2}, {result3}")
    cups.rotate(1)
    destination = cups[0]
    while True:
        destination -= 1
        if destination < min(cups):
            destination = max(cups)
        if destination not in [target1, target2, target3]:
            break
    # print(f"destination: ", destination)
    rot_count = list(cups).index(destination)
    cups.rotate(-rot_count)
    cups.rotate(-1)
    cups.appendleft(target3)
    cups.appendleft(target2)
    cups.appendleft(target1)
    cups.rotate(rot_count)
# print("-- final --")
# print(f"cups: {list(cups)}")
while cups[0] != 1:
    cups.rotate(1)
cups.popleft()
print(f"Part 1: result is {''.join(list(map(str, cups)))}")


# Part 2 - deque is too slow. Use a dict instead as a mini linked list.
cups = [int(c) for c in raw_cups]
cups += list(range(max(cups) + 1, 1_000_000 + 1))
N_TURNS = 10_000_000
cup_links: Dict[int, int] = {cups[i - 1]: cups[i] for i in range(1, len(cups))}
cup_links[cups[-1]] = cups[0]
current_cup = cups[0]
min_cup = min(cups)
max_cup = max(cups)

for _ in range(N_TURNS):
    target1 = cup_links[current_cup]
    target2 = cup_links[target1]
    target3 = cup_links[target2]
    next_cup = cup_links[target3]
    cup_links[current_cup] = next_cup
    destination = current_cup
    while True:
        destination -= 1
        if destination < min_cup:
            destination = max_cup
        if destination not in [target1, target2, target3]:
            break
    cup_links[target3] = cup_links[destination]
    cup_links[destination] = target1
    current_cup = next_cup
product = cup_links[1] * cup_links[cup_links[1]]
print(f"Part 2: product is {product}")
