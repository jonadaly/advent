import itertools
from pathlib import Path
import numpy as np

raw_input = Path("08.txt").read_text().strip().split("\n")
city = np.array([list(line) for line in raw_input], dtype=str)

antenna_locations = {
    str(char): [complex(y, x) for y, x in zip(*np.where(city == char))]
    for char in set(city.flatten()) - {"."}
}


def is_in_bounds(node: complex) -> bool:
    return 0 <= node.real < city.shape[0] and 0 <= node.imag < city.shape[1]


def find_antinodes(
    antenna_1: complex, antenna_2, consider_harmonics: bool
) -> set[complex]:
    difference = antenna_1 - antenna_2
    max_possible_harmonics = abs(
        min(int(city.shape[0] / difference.real), int(city.shape[1] / difference.imag))
    )
    my_range = range(0, max_possible_harmonics) if consider_harmonics else range(1, 2)
    candidates_after = [antenna_1 + difference * i for i in my_range]
    candidates_before = [antenna_2 - difference * i for i in my_range]
    return {n for n in candidates_after + candidates_before if is_in_bounds(n)}


antinodes = set()
antinodes_with_harmonics = set()
for antenna_type, locations in antenna_locations.items():
    # Iterate over all pairs of antenna.
    for i, j in itertools.combinations(locations, r=2):
        antinodes |= find_antinodes(i, j, consider_harmonics=False)
        antinodes_with_harmonics |= find_antinodes(i, j, consider_harmonics=True)

print(f"Part 1: There are {len(antinodes)} antinodes")
print(f"Part 2: There are {len(antinodes_with_harmonics)} antinodes with harmonics")
