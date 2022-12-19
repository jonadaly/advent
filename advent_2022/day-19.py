from dataclasses import dataclass, field, replace
from enum import Enum
from functools import cache
from pathlib import Path
import re
from typing import Generator, Optional

blueprints_raw: list[str] = Path("day-19-example.txt").read_text().strip().split("\n")


def parse_blueprint(raw: str) -> tuple:
    return tuple(map(int, re.findall(r"\d+", raw)))


blueprints = list(map(parse_blueprint, blueprints_raw))

MAX_THEORETICAL = [
    0,
    0,
    1,
    3,
    6,
    10,
    15,
    21,
    28,
    36,
    45,
    55,
    66,
    78,
    91,
    105,
    120,
    136,
    153,
    171,
    190,
    210,
    231,
    253,
    276,
]


@dataclass
class State:
    total: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    active: list[int] = field(default_factory=lambda: [1, 0, 0, 0])

    def __repr__(self):
        return f"State(total={self.total}, active={self.active})"

    def copy(self):
        return State(total=self.total.copy(), active=self.active.copy())


def tick(_state):
    _state.total[0] += _state.active[0]
    _state.total[1] += _state.active[1]
    _state.total[2] += _state.active[2]
    _state.total[3] += _state.active[3]


def simulate(
    remaining: int,
    blueprint: tuple,
    state: State,
    trail: list,
    delayed_add: Optional[list] = None,
) -> Generator[State, None, None]:
    highest_cost_ore = max(
        *blueprint[:4], blueprint[5]
    )
    global best_so_far

    while remaining > 0:

        # Optimise - can't possibly make enough
        if (
            state.total[3] + state.active[3] * remaining + MAX_THEORETICAL[remaining]
            <= best_so_far
        ):
            return

        # Optimise - too much stuff
        if (
            state.total[0] > highest_cost_ore * remaining
            # or state.total[1] > blueprint.obsidian_robot_cost_clay * remaining
            # or state.total[2] > blueprint.geode_robot_cost_obsidian * remaining
        ):
            return

        remaining -= 1

        # print(f"Loop - remaining {remaining}")
        tick(state)

        if delayed_add:
            state.active[0] += delayed_add[0]
            state.active[1] += delayed_add[1]
            state.active[2] += delayed_add[2]
            state.active[3] += delayed_add[3]
            delayed_add = None

        trail.append(f"Minute {24-remaining}: {remaining} mins left " + str(state))

        # print(state)

        if (
            state.total[0] >= blueprint[5]
            and state.total[2] >= blueprint[6]
            and state.active[2] > 0
        ):
            # print("Buying geode bot")
            copy_state = state.copy()
            copy_state.total[0] -= blueprint[5]
            copy_state.total[2] -= blueprint[6]
            trail.append("Bought geode bot " + str(copy_state))
            yield from simulate(
                remaining=remaining,
                blueprint=blueprint,
                state=copy_state,
                trail=trail.copy(),
                delayed_add=[0, 0, 0, 1],
            )
            trail.pop()

        if (
            state.total[0] >= blueprint[3]
            and state.total[1] >= blueprint[4]
            and state.active[1] > 0
            and state.active[2] < blueprint[6]
        ):
            # print("Buying obsidian bot")
            copy_state = state.copy()
            copy_state.total[0] -= blueprint[3]
            copy_state.total[1] -= blueprint[4]
            trail.append("Bought obsidian bot " + str(copy_state))
            yield from simulate(
                remaining=remaining,
                blueprint=blueprint,
                state=copy_state,
                trail=trail.copy(),
                delayed_add=[0, 0, 1, 0],
            )
            trail.pop()

        if (
            state.total[0] >= blueprint[2]
            and state.total[0]
            and state.active[1] < blueprint[4]
        ):
            # print("Buying clay bot")
            copy_state = state.copy()
            copy_state.total[0] -= blueprint[2]
            trail.append("Bought clay bot " + str(copy_state))
            yield from simulate(
                remaining=remaining,
                blueprint=blueprint,
                state=copy_state,
                trail=trail.copy(),
                delayed_add=[0, 1, 0, 0],
            )
            trail.pop()

        if (
            state.total[0] >= blueprint[1]
            and state.active[0] < highest_cost_ore
        ):
            # print("Buying ore bot")
            copy_state = state.copy()
            copy_state.total[0] -= blueprint[1]
            trail.append("Bought ore bot " + str(copy_state))
            yield from simulate(
                remaining=remaining,
                blueprint=blueprint,
                state=copy_state,
                trail=trail.copy(),
                delayed_add=[1, 0, 0, 0],
            )
            trail.pop()

    if state.total[3] > best_so_far:
        print("New best:", "\n", state.total[3], "\n", state)
        import pprint

        pprint.pprint(trail)
        best_so_far = state.total[3]
    yield state


best_so_far = 0

# states = list(simulate(remaining=24, blueprint=blueprints[0], state=State(), trail=[f"24 left "+ str(State())]))

total_quality_level = 0
for blueprint in blueprints:
    best_so_far = 0
    states = simulate(
        remaining=24,
        blueprint=blueprint,
        state=State(),
        trail=[f"24 left " + str(State())],
    )
    list(states)
    quality_level = blueprint[0] * best_so_far
    print(
        f"Blueprint {blueprint[0]}: best is {best_so_far} (quality level {quality_level})"
    )
    total_quality_level += quality_level
print(f"Part 1: total quality level is {total_quality_level}")
