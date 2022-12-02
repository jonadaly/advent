from pathlib import Path

rounds: list[str] = Path("day-02-input.txt").read_text().strip().split("\n")


# This is dumb but I wanted to use match/case.
points = {"X": 1, "Y": 2, "Z": 3}
total_points = 0
for round in rounds:
    them, us = round.split(" ")
    total_points += points[us]
    match (them, us):
        case ("A", "Y") | ("B", "Z") | ("C", "X"):  # win
            total_points += 6
        case ("A", "X") | ("B", "Y") | ("C", "Z"):  # draw
            total_points += 3
print(f"Part 1: Points total is {total_points}")

# This is even dumber but whatever.
points = {"A": 1, "B": 2, "C": 3}
total_points = 0
for round in rounds:
    them, outcome = round.split(" ")
    if outcome == "X":  # loss
        total_points += 1 + (points[them] + 1) % 3
    elif outcome == "Y":  # draw
        total_points += 3 + points[them]
    else:  # win
        total_points += 7 + (points[them]) % 3

print(f"Part 2: Points total is {total_points}")
