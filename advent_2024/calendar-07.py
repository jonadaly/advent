import operator
from pathlib import Path
from itertools import product
from typing import Callable

raw_ops = Path("07.txt").read_text().strip().split("\n")


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_valid_sum(
    result: int, operands: list[int], operators: list[Callable[[int, int], int]]
) -> bool:
    combs = list(product(operators, repeat=len(operands) - 1))
    possible_results = []
    for c in combs:
        ptr = 0
        running = operands[ptr]
        for op in c:
            running = op(running, operands[ptr + 1])
            ptr += 1
        possible_results.append(running)
    return result in possible_results


def solve(allow_concat: bool) -> int:
    operators = [operator.mul, operator.add]
    if allow_concat:
        operators.append(concat)
    total = 0
    for raw_op in raw_ops:
        result, raw_operands = raw_op.split(":")
        operands = list(map(int, raw_operands.strip().split()))
        if is_valid_sum(int(result), operands, operators):
            total += int(result)
    return total


print(f"Part 1: Total is {solve(allow_concat=False)}")
print(f"Part 2: Total is {solve(allow_concat=True)}")
