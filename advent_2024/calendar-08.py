import itertools
from pathlib import Path
import numpy as np

raw_input = Path("08.txt").read_text().strip().split("\n")
city = np.array([list(line) for line in raw_input], dtype=str)

antenna_locations = {
    str(char): [complex(y, x) for y, x in zip(*np.where(city == char))]
    for char in set(city.flatten()) - {"."}
}


def find_antinodes(
    antenna_1: complex, antenna_2, consider_harmonics: bool
) -> set[complex]:
    difference = antenna_1 - antenna_2
    new_antinodes = {antenna_1, antenna_2} if consider_harmonics else set()
    current_node = antenna_1
    while True:
        next_node = current_node + difference
        if (
            next_node.real >= city.shape[0]
            or next_node.real < 0
            or next_node.imag >= city.shape[1]
            or next_node.imag < 0
        ):
            break
        new_antinodes.add(next_node)
        current_node = next_node
        if not consider_harmonics:
            break

    current_node = antenna_2
    while True:
        next_node = current_node - difference
        if (
            next_node.real >= city.shape[0]
            or next_node.real < 0
            or next_node.imag >= city.shape[1]
            or next_node.imag < 0
        ):
            break
        new_antinodes.add(next_node)
        current_node = next_node
        if not consider_harmonics:
            break
    return new_antinodes


antinodes = set()
antinodes_with_harmonics = set()
for antenna_type, locations in antenna_locations.items():
    # Iterate over all pairs of antenna.
    for i, j in itertools.combinations(locations, r=2):
        antinodes |= find_antinodes(i, j, consider_harmonics=False)
        antinodes_with_harmonics |= find_antinodes(i, j, consider_harmonics=True)

print(f"Part 1: There are {len(antinodes)} antinodes")
print(f"Part 2: There are {len(antinodes_with_harmonics)} antinodes with harmonics")
