import operator
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Callable

Operator = Callable[[int, int], int]

OPERATORS: dict[str, Operator] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


@dataclass
class Monkey:
    id: int
    items: list[int]
    _operator: str
    operand: str
    test_divisor: int
    test_true: int
    test_false: int
    inspections: int = 0

    def inspect(self, old: int) -> int:
        # eval() is evil and slow, so we do it properly.
        _op: Operator = OPERATORS[self._operator]
        return _op(old, old if self.operand == "old" else int(self.operand))

    def target(self, x: int) -> int:
        return self.test_true if x % self.test_divisor == 0 else self.test_false


monkeys_raw: list[str] = Path("day-11-input.txt").read_text().strip().split("\n\n")

monkeys: dict[int, Monkey] = {}
for id, monkey_raw in enumerate(monkeys_raw):
    monkey_lines = monkey_raw.split("\n")
    _operator, operand = monkey_lines[2].split("= old ")[-1].split()
    monkeys[id] = Monkey(
        id=id,
        items=list(map(int, monkey_lines[1].split(": ")[-1].split(","))),
        _operator=_operator,
        operand=operand,
        test_divisor=int(monkey_lines[3].split("by ")[-1]),
        test_true=int(monkey_lines[4].split("monkey ")[-1]),
        test_false=int(monkey_lines[5].split("monkey ")[-1]),
    )

common_factor: int = reduce(
    (lambda x, y: x * y), [m.test_divisor for m in monkeys.values()]
)


def simulate(monkeys: dict[int, Monkey], *, rounds: int, relief: int) -> int:
    _monkeys = deepcopy(monkeys)  # Don't mutate input.
    for _ in range(rounds):
        for monkey in _monkeys.values():
            for item in monkey.items:
                monkey.inspections += 1
                worry_level = monkey.inspect(item) // relief
                # Divide by common factor to avoid ridiculous numbers.
                worry_level %= common_factor
                throw_target = monkey.target(worry_level)
                _monkeys[throw_target].items.append(worry_level)
            monkey.items = []
    inspections = sorted(monkey.inspections for monkey in _monkeys.values())
    return inspections[-2] * inspections[-1]


print(f"Part 1: Monkey business is {simulate(monkeys, rounds=20, relief=3)}")
print(f"Part 1: Monkey business is {simulate(monkeys, rounds=10_000, relief=1)}")
