import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Generator

valves_raw: list[str] = Path("day-16-input.txt").read_text().strip().split("\n")


@dataclass
class Valve:
    id: str
    flow_rate: int
    children: list[str]

    @classmethod
    def parse_raw(cls, raw: str) -> "Valve":
        match = re.match(r"^Valve (.*) has flow rate=(\d+); .* valves? (.*)", raw)
        if match is None:
            raise ValueError(f"Invalid valve: {raw}")
        valve_id, valve_flow_rate, valve_tunnels = match.groups()
        return Valve(
            id=valve_id,
            flow_rate=int(valve_flow_rate),
            children=valve_tunnels.split(", "),
        )


@dataclass
class State:
    steps: int = 0
    flow_rate: int = 0
    total: int = 0


def solve_for(
    position: str, remaining_minutes: int, opened_valves: tuple[str, ...]
) -> Generator[tuple[str, ...], None, None]:
    """
    Yields possible paths from the given position, with the given remaining minutes
    and already-opened valves.
    """
    for next in [
        v
        for v in valves.values()
        if (
            v.id != position
            and v.id not in opened_valves
            and v.flow_rate > 0
            and distances[position][v.id] < remaining_minutes
        )
    ]:
        yield from solve_for(
            next.id,
            remaining_minutes - distances[position][next.id] - 1,
            (*opened_valves, next.id),
        )
    yield opened_valves


def score_path(path: tuple[str, ...], remaining: int) -> int:
    """
    Scores a given path by taking into account the distance between valves
    and the flow rate contributed by each valve.
    """
    total = 0
    flow_rate = 0
    curr = "AA"
    for valve in path:
        remaining -= distances[curr][valve] + 1
        total += (distances[curr][valve] + 1) * flow_rate
        flow_rate += valves[valve].flow_rate
        curr = valve
    return total + (flow_rate * remaining)


# Parse valves from input.
valves: dict[str, Valve] = {v.id: v for v in map(Valve.parse_raw, valves_raw)}

# Find distances between each pair of valves. There is an algorithm for this: Floyd-Warshall.
distances: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 999))
# Initialise known distances
for v in valves.keys():
    distances[v][v] = 0
    for c in valves[v].children:
        distances[v][c] = 1
# For each pair of valves, iterate through the other valves and see if we can find a shorter path.
for (i, j, k) in product(valves, valves, valves):
    distances[j][k] = min(distances[j][k], distances[j][i] + distances[i][k])

# Part 1: just need the best scoring path.
paths_p1: list[tuple[str, ...]] = list(
    solve_for(position="AA", remaining_minutes=30, opened_valves=())
)
print(
    f"Part 1: max pressure release is {max(score_path(path, remaining=30) for path in paths_p1)}"
)

# Part 2: need to find a combination of human and elephant paths that don't involve the same valves.
paths_p2 = list(solve_for(position="AA", remaining_minutes=26, opened_valves=()))
# Have to optimise because it would take too long otherwise. We only care about
# the best scoring path for each set of valves - the others will do worse later.
optimised: dict[frozenset[str], int] = defaultdict(int)
for path in paths_p2:
    score: int = score_path(path, remaining=26)
    optimised[frozenset(path)] = max(optimised[frozenset(path)], score)

max_score: int = max(
    optimised[frozenset(human)] + optimised[frozenset(elephant)]
    for human, elephant in product(optimised.keys(), optimised.keys())
    if not set(human) & (set(elephant))
)
print(f"Part 2: max pressure release is {max_score}")
