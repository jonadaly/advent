import string
from pathlib import Path

total_any = 0
total_all = 0
for group in Path("06.txt").read_text().strip().split("\n\n"):
    group_answers_any = set()
    group_answers_all = set(string.ascii_lowercase)
    for person in group.split("\n"):
        group_answers_any = group_answers_any.union(person)
        group_answers_all = group_answers_all.intersection(person)
    total_any += len(group_answers_any)
    total_all += len(group_answers_all)
print(f"Part 1: total is {total_any}")
print(f"Part 2: total is {total_all}")
