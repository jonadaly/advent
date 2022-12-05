import copy
import re
from collections import defaultdict
from pathlib import Path

Stack = dict[int, list[str]]
containers_raw, instructions_raw = Path("day-05-input.txt").read_text().split("\n\n")
instructions_raw = instructions_raw.strip()

stacks: Stack = defaultdict(list)
for container_raw in reversed(containers_raw.split("\n")[:-1]):
    container_marker = 1
    current = 1
    while current < len(container_raw):
        if (curr := container_raw[current]) != " ":
            stacks[container_marker].append(curr)
        container_marker += 1
        current += 4
stacks = dict(stacks)


def move(stacks: Stack, instructions_raw: str, multi: bool) -> Stack:
    result = copy.deepcopy(stacks)
    for instruction_raw in instructions_raw.split("\n"):
        match = re.match(r"move (\d+) from (\d+) to (\d+)", instruction_raw)
        if match is None:
            raise ValueError(f"Invalid instruction: {instruction_raw}")
        num, source, target = tuple(map(int, match.groups()))
        if multi is False:
            for _ in range(num):
                result[target].append(result[source].pop())
        else:
            result[target] += result[source][-num:]
            del result[source][-num:]
    return result


stacks_part1: Stack = move(dict(stacks), instructions_raw, multi=False)
print(f"Part 1: result is {''.join(s[-1] for s in stacks_part1.values())}")

stacks_part2: Stack = move(dict(stacks), instructions_raw, multi=True)
print(f"Part 2: result is {''.join(s[-1] for s in stacks_part2.values())}")
