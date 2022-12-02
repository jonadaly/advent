from pathlib import Path

raw_text = Path("01.txt").read_text().strip()

numbers = [int(n) for n in raw_text.split("\n")]

numbers.sort()

# Part 1
for n in numbers:
    if 2020 - n in numbers:
        print(f"Found numbers {n} and {2020-n}")
        print(f"Numbers multiply to {n*(2020-n)}")
        break

# Part 2
for n in numbers:
    complement = 2020 - n
    for m in numbers:
        if complement - m in numbers:
            print(f"Found numbers {m}, {complement - m}, {n}")
            print(f"Numbers multiply to {m*(complement - m)*n}")
            break
