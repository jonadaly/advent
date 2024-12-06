from pathlib import Path
import numpy as np

raw_input = Path("06.txt").read_text().strip().split("\n")
lab = np.array([list(line) for line in raw_input], dtype=str)

DEBUG = False


def print_situation(lab: np.ndarray, visited_locations: set[tuple[int, int]]):
    if not DEBUG:
        return
    for row in lab:
        print(row.tostring().decode("utf8"))
    print("Visited: ", visited_locations, "\n")


def solve(lab: np.ndarray) -> set[tuple[int, int]]:
    guard_row, guard_col = np.where(lab == "^")
    guard_location = (int(guard_row[0]), int(guard_col[0]))
    visited_locations = {guard_location}
    turning_points = {(guard_location, "^")}
    while True:
        print_situation(lab, visited_locations)
        if lab[guard_location] == "^":
            section = lab[: guard_location[0], guard_location[1]][::-1]
            first_non_empty = next(
                (i for i, c in enumerate(section) if c != "."), len(section)
            )
            visited_locations |= {
                (guard_location[0] - i, guard_location[1])
                for i in range(1, first_non_empty + 1)
            }
            lab[guard_location] = "."
            guard_location = (guard_location[0] - first_non_empty, guard_location[1])
            if (guard_location, ">") in turning_points:
                raise ValueError
            turning_points.add((guard_location, ">"))
            if first_non_empty == len(section):
                break
            lab[guard_location] = ">"
        elif lab[guard_location] == ">":
            section = lab[guard_location[0], guard_location[1] + 1 :]
            first_non_empty = next(
                (i for i, c in enumerate(section) if c != "."), len(section)
            )
            visited_locations |= {
                (guard_location[0], guard_location[1] + i)
                for i in range(1, first_non_empty + 1)
            }
            lab[guard_location] = "."
            guard_location = (guard_location[0], guard_location[1] + first_non_empty)
            if (guard_location, "v") in turning_points:
                raise ValueError
            turning_points.add((guard_location, "v"))
            if first_non_empty == len(section):
                break
            lab[guard_location] = "v"
        elif lab[guard_location] == "v":
            section = lab[guard_location[0] + 1 :, guard_location[1]]
            first_non_empty = next(
                (i for i, c in enumerate(section) if c != "."), len(section)
            )
            visited_locations |= {
                (guard_location[0] + i, guard_location[1])
                for i in range(1, first_non_empty + 1)
            }
            lab[guard_location] = "."
            guard_location = (guard_location[0] + first_non_empty, guard_location[1])
            if (guard_location, "<") in turning_points:
                raise ValueError
            turning_points.add((guard_location, "<"))
            if first_non_empty == len(section):
                break
            lab[guard_location] = "<"
        elif lab[guard_location] == "<":
            section = lab[guard_location[0], : guard_location[1]][::-1]
            first_non_empty = next(
                (i for i, c in enumerate(section) if c != "."), len(section)
            )
            visited_locations |= {
                (guard_location[0], guard_location[1] - i)
                for i in range(1, first_non_empty + 1)
            }
            lab[guard_location] = "."
            guard_location = (guard_location[0], guard_location[1] - first_non_empty)
            if (guard_location, "^") in turning_points:
                raise ValueError
            turning_points.add((guard_location, "^"))
            if first_non_empty == len(section):
                break
            lab[guard_location] = "^"
    print_situation(lab, visited_locations)
    return visited_locations


part1_visited_locations = solve(lab.copy())
print(f"Part 1: visited {len(part1_visited_locations)} locations")


unsolvable = 0
for i, j in part1_visited_locations:
    this_lab = lab.copy()
    if this_lab[i, j] != ".":
        continue
    this_lab[i, j] = "#"
    try:
        part2_visited_locations = solve(this_lab)
    except ValueError:
        unsolvable += 1

print(f"Part 2: {unsolvable} unsolvable cases")
