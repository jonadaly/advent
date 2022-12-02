from pathlib import Path

answers = [g.split("\n") for g in Path("06.txt").read_text().split("\n\n")]
print(sum(len(set(a[0]).union(*a)) for a in answers))
print(sum(len(set(a[0]).intersection(*a)) for a in answers))
