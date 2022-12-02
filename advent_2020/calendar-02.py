import re
from pathlib import Path

raw_text = Path("02.txt").read_text().strip()

rows = raw_text.split("\n")

# Part 1
valid = 0
for row in rows:
    parsed = re.match(r"(\d+)-(\d+) (.): (.*)", row)
    low, high, character, password = parsed.groups()
    if int(low) <= password.count(character) <= int(high):
        valid += 1
print(f"Part 1: {valid} passwords are valid")


# Part 2
valid = 0
for row in rows:
    parsed = re.match(r"(\d+)-(\d+) (.): (.*)", row)
    pos1, pos2, character, password = parsed.groups()
    if (password[int(pos1) - 1] == character) ^ (password[int(pos2) - 1] == character):
        valid += 1
print(f"Part 2: {valid} passwords are valid")
