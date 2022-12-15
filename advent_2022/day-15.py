import re
from pathlib import Path
from typing import Optional

sensors: list[str] = Path("day-15-input.txt").read_text().strip().split("\n")

SEARCH_SPACE = 2_000_000
all_beacons = []
all_sensors = []
for sensor in sensors:
    match = re.match(
        r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
        sensor,
    )
    if match is None:
        raise ValueError(f"Invalid sensor: {sensor}")
    sensor_x, sensor_y, beacon_x, beacon_y = map(int, match.groups())
    all_sensors.append((sensor_x, sensor_y))
    all_beacons.append((beacon_x, beacon_y))


def find_impossible_positions(i_row: int):
    """Calculates the ranges of x values that are impossible for the beacons to occupy""" ""
    taken: list[tuple[int, int]] = []
    for i in range(len(all_sensors)):
        sensor_x, sensor_y = all_sensors[i]
        beacon_x, beacon_y = all_beacons[i]
        manhattan_distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        slack = manhattan_distance - abs(i_row - sensor_y)
        if slack >= 0:
            taken.append((sensor_x - slack, sensor_x + slack))
    return taken


def combine(
    all: list[tuple[int, int]], limit: Optional[int] = None
) -> list[tuple[int, int]]:
    """Combines a list of ranges into as few ranges as possible."""
    all.sort()
    new_ranges = []
    left, right = all[0]
    for next_left, next_right in all[1:]:
        if right + 1 < next_left:
            new_ranges.append((left, right))
            left, right = next_left, next_right
        else:
            right = max(right, next_right)
    new_ranges.append((left, right))
    if limit is None:
        return new_ranges
    updated_ranges = []
    for x, y in new_ranges:
        if x > limit:
            continue
        if y > limit:
            y = limit
        updated_ranges.append((x, y))
    return updated_ranges


taken_p1 = find_impossible_positions(SEARCH_SPACE)
total = sum(r[1] - r[0] + 1 for r in combine(taken_p1)) - sum(
    1 for s in set(all_sensors) | set(all_beacons) if s[1] == SEARCH_SPACE
)
print(f"Part 1: {total} spaces where beacon cannot be present on row {SEARCH_SPACE}")

# Part 2 takes about 20 seconds to run.
for i_row in range(SEARCH_SPACE * 2):
    taken = find_impossible_positions(i_row)
    combined_range = combine(taken, limit=SEARCH_SPACE * 2)
    if len(combined_range) > 1:
        # There's a gap in the range.
        print(
            f"Part 2: tuning frequency is {(combined_range[0][1] + 1)*SEARCH_SPACE*2 + i_row}"
        )
        break
