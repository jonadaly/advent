from typing import Counter
from pathlib import Path
import re

raw_machines = Path("14.txt").read_text().strip().split("\n")
WIDTH = 101
HEIGHT = 103

machines = []
for raw_machine in raw_machines:
    raw_match = re.match(r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$", raw_machine)
    p1, p2, v1, v2 = map(int, raw_match.groups())  # type: ignore
    machines.append((complex(p1, p2), complex(v1, v2)))


def print_robots(state):
    counter = dict(Counter([m[0] for m in state]))
    for y in range(HEIGHT):
        print("".join([str(counter.get(complex(i, y), ".")) for i in range(WIDTH)]))
    print("\n")


def calc_safety_factor(state):
    NE_count = sum(
        [1 for m in state if m[0].real < WIDTH // 2 and m[0].imag < HEIGHT // 2]
    )
    NW_count = sum(
        [1 for m in state if m[0].real < WIDTH // 2 and m[0].imag > HEIGHT // 2]
    )
    SE_count = sum(
        [1 for m in state if m[0].real > WIDTH // 2 and m[0].imag < HEIGHT // 2]
    )
    SW_count = sum(
        [1 for m in state if m[0].real > WIDTH // 2 and m[0].imag > HEIGHT // 2]
    )
    return NE_count * NW_count * SE_count * SW_count


state = machines
min_safety_factor = float("inf")
idx_min_safety_factor = -1
all_states = []
for i in range(10_000):
    new_state = []
    for m in state:
        new_x = (m[0].real + m[1].real) % WIDTH
        new_y = (m[0].imag + m[1].imag) % HEIGHT
        new_state.append((complex(new_x, new_y), m[1]))
        state = new_state
    safety_factor = calc_safety_factor(state)
    if safety_factor < min_safety_factor:
        min_safety_factor = safety_factor
        idx_min_safety_factor = i
    all_states.append(state)


print_robots(all_states[idx_min_safety_factor])
print(f"Part 1: safety factor after 100 s is {calc_safety_factor(all_states[99])}")
# Assume Christmas tree in the pattern means a low safety factor, because robots are going to be close together somewhere
print(f"Part 2: xmas tree after {idx_min_safety_factor+1} seconds")
