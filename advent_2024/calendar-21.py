from functools import cache
from pathlib import Path


codes = Path("21.txt").read_text().strip().split("\n")

keypad = {
    "7": 0 + 0j,
    "8": 1 + 0j,
    "9": 2 + 0j,
    "4": 0 + 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "1": 0 + 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    " ": 0 + 3j,
    "0": 1 + 3j,
    "A": 2 + 3j,
}
arrowpad = {
    " ": 0 + 0j,
    "^": 1 + 0j,
    "A": 2 + 0j,
    "<": 0 + 1j,
    "v": 1 + 1j,
    ">": 2 + 1j,
}


@cache
def find_seq(start: str, end: str) -> str:
    pad = keypad if (start in keypad and end in keypad) else arrowpad
    vector = pad[end] - pad[start]
    dx, dy = int(vector.real), int(vector.imag)
    vertical = ("^" * -dy) + ("v" * dy)
    horizontal = ("<" * -dx) + (">" * dx)
    bad = pad[" "] - pad[start]
    # Through trial and error, if moving to the right or space key horizontally aligns with our target, then do vertical moves first
    # UNLESS the space key is on the same vertical line as start + dy
    vertical_first = (dx > 0 or bad.real == dx) and bad != dy * 1j
    return (vertical + horizontal if vertical_first else horizontal + vertical) + "A"


@cache
def count_steps(code: str, level: int) -> int:
    if level < 0:
        return len(code)
    return sum(
        count_steps(find_seq(code[idx - 1], step), level - 1)
        for idx, step in enumerate(code)
    )


total_p1 = sum(count_steps(code, 2) * int(code[:-1]) for code in codes)
total_p2 = sum(count_steps(code, 25) * int(code[:-1]) for code in codes)

print(f"Part 1: total complexity is {total_p1}")
print(f"Part 2: total complexity is {total_p2}")
