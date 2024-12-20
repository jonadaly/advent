from collections import Counter
from pathlib import Path


raw_input = Path("20.txt").read_text().strip().split("\n")
track = [list(line) for line in raw_input]
start = next(
    complex(i, j) for i, row in enumerate(track) for j, c in enumerate(row) if c == "S"
)
end = next(
    complex(i, j) for i, row in enumerate(track) for j, c in enumerate(row) if c == "E"
)

race_path = [start]
while True:
    if race_path[-1] == end:
        break
    for direction in [-1, 1, -1j, 1j]:
        new_pos = race_path[-1] + direction
        if (
            new_pos in race_path
            or track[int(new_pos.real)][int(new_pos.imag)] == "#"
            or new_pos.real < 0
            or new_pos.imag < 0
            or new_pos.real >= len(track)
            or new_pos.imag >= len(track[0])
        ):
            continue
        race_path.append(new_pos)
race_path_map = {p: i for i, p in enumerate(race_path)}


def manhattan_distance(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def get_cheats(cheat_range: int) -> Counter[int]:
    # There's an easier/faster way to do this by comparing pairs of points on the track and checking
    # whether the Manhattan distance is less than cheat_range, but I'm too lazy to do that now.
    seqs = {
        complex(i, j)
        for i in range(-cheat_range, cheat_range + 1)
        for j in range(-cheat_range, cheat_range + 1)
        if (i != 0 or j != 0) and (manhattan_distance(0, complex(i, j)) <= cheat_range)
    }

    cheats: dict[tuple[complex, complex], int] = {}
    for pos, i in race_path_map.items():
        for seq in seqs:
            cheat_end = pos + seq
            if cheat_end not in race_path_map:
                continue
            saved = race_path_map[cheat_end] - i - (manhattan_distance(pos, cheat_end))
            if cheats.get((pos, cheat_end), 0) < saved:
                cheats[(pos, cheat_end)] = saved
    return Counter(cheats.values())


part1_sorted_cheats = dict(sorted(get_cheats(2).items()))
part1_cheats = sum(v for k, v in part1_sorted_cheats.items() if k >= 100)
print(f"Part 1: {part1_cheats} cheats save over 100 picoseconds")

part2_sorted_cheats = dict(sorted(get_cheats(20).items()))
part2_cheats = sum(v for k, v in part2_sorted_cheats.items() if k >= 100)
print(f"Part 2: {part2_cheats} cheats save over 100 picoseconds")
