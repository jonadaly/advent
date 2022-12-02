from pathlib import Path

elves_raw: list[str] = Path("day-01-input.txt").read_text().strip().split("\n\n")
elves_parsed: list[list[int]] = [list(map(int, e.split("\n"))) for e in elves_raw]
elf_totals: list[int] = sorted(map(sum, elves_parsed), reverse=True)  # type: ignore

print(f"Part 1: top elf carries {elf_totals[0]} calories")
print(f"Part 2: top three elves carry {sum(elf_totals[:3])} calories")
