from dataclasses import dataclass
from pathlib import Path

jets: str = Path("day-17-input.txt").read_text().strip()

rocks = [
    (0, 1, 2, 3),
    (1, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0, 1, 2, 2 + 1j, 2 + 2j),
    (0, 0 + 1j, 0 + 2j, 0 + 3j),
    (0, 1, 0 + 1j, 1 + 1j),
]

ROCK_HEIGHTS = [1, 3, 3, 4, 2]


@dataclass
class State:
    height: int = 0
    i_jet: int = 0
    i_rock: int = 0


def check(rock, rock_coords, column, jet_nudge):
    for local in rock:
        new_position = local + rock_coords + jet_nudge
        if (
            new_position.real > 6
            or new_position.real < 0
            or new_position.imag < 0
            or new_position in column
        ):
            return False
    return True


column: list[complex] = []
previous: dict[tuple[int, int], tuple[int, int]] = {}  # Yeah I know...
state = State()
for i in range(int(1e12)):
    rock = rocks[state.i_rock]
    rock_coords = complex(2, state.height + 3)

    # Do some caching to speed things up.
    if (state.i_rock, state.i_jet) in previous:
        last_i, last_height = previous[(state.i_rock, state.i_jet)]
        rem = (int(1e12) - i) % (i - last_i)
        cycles = (int(1e12) - i) // (i - last_i)
        if rem == 0:
            # Keep going until we find the exact match for 1e12, since it makes life easier.
            new_height = state.height + cycles * (state.height - last_height)
            print(f"Part 2: height is {new_height}")
            break
    previous[(state.i_rock, state.i_jet)] = (i, state.height)

    while True:
        jet_nudge = 1 if jets[state.i_jet] == ">" else -1
        state.i_jet = (state.i_jet + 1) % len(jets)
        if check(rock, rock_coords, column, jet_nudge):
            rock_coords += jet_nudge
        if check(rock, rock_coords, column, -1j):
            rock_coords -= 1j
        else:
            break
    column += [rock_coords + r for r in rock]

    # Update state
    state.height = int(max(state.height, rock_coords.imag + ROCK_HEIGHTS[state.i_rock]))
    state.i_rock = (state.i_rock + 1) % len(rocks)

    # Part 1 answer
    if i == 2022:
        print(f"Part 1: height after 2022 rocks is {state.height}")
