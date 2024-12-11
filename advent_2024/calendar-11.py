import functools
from pathlib import Path

raw_input = Path("11.txt").read_text().strip()
stones = list(map(int, raw_input.split()))


@functools.cache
def solve_stone(_stone: int, n: int) -> int:
    if n == 0:
        return 1
    if _stone == 0:
        return solve_stone(1, n - 1)
    if len((str_s := str(_stone))) % 2 == 0:
        stone_1 = int(str_s[: len(str_s) // 2])
        stone_2 = int(str_s[len(str_s) // 2 :])
        return solve_stone(stone_1, n - 1) + solve_stone(stone_2, n - 1)
    return solve_stone(_stone * 2024, n - 1)


print(f"Part 1: {sum((solve_stone(s, 25)) for s in stones)}")
print(f"Part 2: {sum((solve_stone(s, 75)) for s in stones)}")
