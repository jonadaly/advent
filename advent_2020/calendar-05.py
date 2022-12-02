from pathlib import Path

# Part 1
seat_ids = []
for boarding_pass in Path("05.txt").read_text().strip().split("\n"):
    binary_row = boarding_pass[:7].replace("B", "1").replace("F", "0")
    binary_col = boarding_pass[7:].replace("R", "1").replace("L", "0")
    seat_ids.append(int(binary_row, 2) * 8 + int(binary_col, 2))
print(f"Part 1: highest ID is {max(seat_ids)}")

# Part 2
missing = set(range(128 * 8)) - set(seat_ids)
my_seat = next(s for s in missing if s - 1 not in missing and s + 1 not in missing)
print(f"Part 2: my seat is {my_seat}")
