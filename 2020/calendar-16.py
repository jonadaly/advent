from pathlib import Path
import re
from typing import Dict, Set, List
from collections import defaultdict
import numpy as np

raw_lines = Path("16.txt").read_text().strip().split("\n\n")
fields: Dict[int, Set[int]] = {}
any_field_validity = set()
for raw_field in raw_lines[0].split("\n"):
    groups = re.match(r"^(.+): (\d+)-(\d+) or (\d+)-(\d+)$", raw_field).groups()
    fields[groups[0]] = set(range(int(groups[1]), int(groups[2]) + 1)) | set(
        range(int(groups[3]), int(groups[4]) + 1)
    )
    any_field_validity |= fields[groups[0]]
invalid_value_total = 0
valid_tickets: List[List[int]] = []
for other_ticket in raw_lines[2].split("\n")[1:]:
    all_valid = True
    values = list(map(int, other_ticket.split(",")))
    for v in values:
        if v not in any_field_validity:
            invalid_value_total += v
            all_valid = False
    if all_valid:
        valid_tickets.append(values)
print(f"Part 1: sum of invalid values is {invalid_value_total}")

valid_values_per_field: Dict[int, Set[int]] = defaultdict(set)
for valid_ticket in valid_tickets:
    for i, value in enumerate(valid_ticket):
        valid_values_per_field[i].add(value)

field_map: Dict[int, str]= {}
while True:
    if len(field_map) == len(fields):
        break
    for k, v in valid_values_per_field.items():
        candidate_fields = [k2 for k2, v2 in fields.items() if v <= v2 and k2 not in field_map.values()]
        if len(candidate_fields) == 1:
            # Found a single match.
            field_map[k] = candidate_fields[0]
            continue
# print(f"Found field map: {field_map}")

my_ticket = list(map(int, raw_lines[1].split("\n")[1].split(",")))
product_values = np.product([my_ticket[k] for k, v in field_map.items() if v.startswith("departure")])
print(f"Part 2: Product of my departure fields is {product_values}")
