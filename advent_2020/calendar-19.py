import re
from pathlib import Path


def parse_rule(all_rules, i_rule, part2=False):
    rule_to_parse = all_rules[i_rule]
    if part2:
        if i_rule == 8:
            return "(" + parse_rule(all_rules, 42, part2=True) + ")+"
        if i_rule == 11:
            r42 = parse_rule(all_rules, 42, part2=True)
            r31 = parse_rule(all_rules, 31, part2=True)
            options = [r42 + f"{{{i}}}" + r31 + f"{{{i}}}" for i in range(1, 10)]
            return "(" + "|".join(options) + ")"
    if rule_to_parse.startswith('"'):
        return rule_to_parse[1:-1]
    branches = rule_to_parse.split("|")
    regexes = []
    for branch in branches:
        sub_regexes = []
        # print(branch, "...", branch.strip().split(" "))
        sub_rules = branch.strip().split(" ")
        for sr in sub_rules:
            parsed_sub_rule = parse_rule(all_rules, int(sr), part2=part2)
            sub_regexes.append(parsed_sub_rule)
        # print("regexes from branch: ", sub_regexes)
        regexes.append("".join(sub_regexes))
    # print(f"rule {i_rule} is regex from sub_rules: ", "|".join(regexes))
    return "(" + "|".join(regexes) + ")"


sections = Path("19.txt").read_text().strip().split("\n\n")
raw_rules = sections[0].split("\n")
messages = sections[1].split("\n")

rules = {}
for raw_rule in raw_rules:
    groups = re.match(r"^(\d+): (.+)$", raw_rule).groups()
    rules[int(groups[0])] = groups[1]

# Part 1
parsed_rule = "^" + parse_rule(rules, 0) + "$"
total = 0
for message in messages:
    match = re.match(parsed_rule, message)
    if match is not None:
        total += 1
print(f"Part 1: total is {total}")


# Part 2 - slow (1 min)
parsed_rule = "^" + parse_rule(rules, 0, part2=True) + "$"
total = 0
for imes, message in enumerate(messages):
    match = re.match(parsed_rule, message)
    if match is not None:
        total += 1
    # print(f"Done message {imes} of {len(messages)}")
print(f"Part 2: total is {total}")
