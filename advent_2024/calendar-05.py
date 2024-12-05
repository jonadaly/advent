from collections import defaultdict
from pathlib import Path

# Parse the input
raw_rules, raw_updates = Path("05.txt").read_text().strip().split("\n\n")
updates = [
    list(map(int, raw_update.split(","))) for raw_update in raw_updates.split("\n")
]
dependencies = defaultdict(list)
for rule in raw_rules.split("\n"):
    a, b = rule.split("|")
    dependencies[int(b)].append(int(a))


def check_valid(update: list[int]) -> bool:
    for i, curr in enumerate(update):
        the_rest = update[i + 1 :]
        if any(dependency in the_rest for dependency in dependencies[curr]):
            return False
    return True


def reorder(update: list[int]) -> list[int]:
    working = update[:]
    i = 0
    while i < len(working):
        curr = working[i]
        for dependency in dependencies[curr]:
            if dependency in working and working.index(dependency) > i:
                working.remove(dependency)
                working.insert(i, dependency)
                i = -1  # Go back one character and recheck from there
                break
        i += 1
    return working


def reorder_2(update: list[int]) -> list[int]:
    # A more readable version (but slightly less efficient because of the repeated list creation)
    while True:
        working = update[:]
        for i, curr in enumerate(working):
            for dependency in dependencies[curr]:
                if dependency in working and working.index(dependency) > i:
                    working.remove(dependency)
                    working.insert(i, dependency)
                    break
        if update == working:
            return working
        update = working


valid_updates = [u for u in updates if check_valid(u)]
sum_of_middle = sum([v[len(v) // 2] for v in valid_updates])
print(f"Part 1: sum of middle page numbers of valid updates is {sum_of_middle}")

invalid_updates = [u for u in updates if not check_valid(u)]
reordered_updates = [reorder(u) for u in invalid_updates]
sum_of_middle = sum([v[len(v) // 2] for v in reordered_updates])
print(f"Part 2: sum of middle page numbers of reordered updates is {sum_of_middle}")
