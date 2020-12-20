from pathlib import Path
import re
import regex_engine

generate = regex_engine.generator()

REQUIRED_FIELDS = {
    "byr": generate.numerical_range(1920, 2002),
    "iyr": generate.numerical_range(2010, 2020),
    "eyr": generate.numerical_range(2020, 2030),
    "hgt": f"({generate.numerical_range(150, 193)[:-1]}cm$)|({generate.numerical_range(59, 76)[:-1]}in$)",
    "hcl": r"^#[0-9a-fA-F]{6}$",
    "ecl": r"^amb|blu|brn|gry|grn|hzl|oth$",
    "pid": r"^\d{9}$",
}

passports = Path("4.txt").read_text().strip().split("\n\n")

# Part 1
valid = 0
for passport in passports:
    fields = {f[:3]: f[4:] for f in passport.split()}
    if REQUIRED_FIELDS.keys() <= set(fields.keys()):
        valid += 1
print(f"Part 1: {valid} passports are valid")

# Part 2
valid = 0
for passport in passports:
    fields = {f[:3]: f[4:] for f in passport.split()}
    if all(
        re.match(reg, fields.get(key, "")) is not None
        for key, reg in REQUIRED_FIELDS.items()
    ):
        valid += 1
print(f"Part 2: {valid} passports are valid")
