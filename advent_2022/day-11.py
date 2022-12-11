from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Callable


@dataclass
class Monkey:
    _id: int
    _items: list[int]
    _operation: Callable[[int], int]
    _test: Callable[[int], int]
    inspections: int = 0

    def __repr__(self) -> str:
        return f"""Monkey {self._id}
        Items: {self._items}
        Operation: {self._operation}
        test: {self._test}
        inspections: {self.inspections}
        """


divisors = []
monkeys: dict[int, Monkey] = {}
monkeys_raw: list[str] = Path("day-11-input.txt").read_text().strip().split("\n\n")
for id, monkey_raw in enumerate(monkeys_raw):
    monkey_lines = monkey_raw.split("\n")
    starting_items = list(map(int, monkey_lines[1].split(":")[-1].strip().split(",")))
    operation_parse = monkey_lines[2].split("new = old")[-1].strip().split()
    operation: Callable[[int], int] = eval(
        f"lambda old: old {operation_parse[0]} {operation_parse[1]}"
    )
    test_div_by = int(monkey_lines[3].split("by")[-1].strip())
    divisors.append(test_div_by)
    test_true = int(monkey_lines[4].split("monkey ")[-1])
    test_false = int(monkey_lines[5].split("monkey ")[-1])
    print(f"Monkey {id}: if div by {test_div_by} then {test_true} else {test_false}")
    test: Callable[[int], int] = (
        lambda x, t=test_true, f=test_false, d=test_div_by: t if x % d == 0 else f  # type: ignore
    )
    monkeys[id] = Monkey(
        _id=id, _items=starting_items, _operation=operation, _test=test
    )

print(monkeys)

common_factor = reduce((lambda x, y: x * y), divisors)

history_inspections_this_found: list[list[int]] = []
permutations: list[tuple[int, list[int]]] = []
for round in range(10000):
    inspections_this_round = []
    print(f"round {round}")
    for __id, monkey in monkeys.items():
        # print(f"Doing monkey {__id}")
        # if __id == 0: print(len(monkey._items))
        for item in monkey._items:
            # print(f"Doing item {item}")
            monkey.inspections += 1
            worry_level = monkey._operation(item)
            worry_level = worry_level % common_factor
            throw_target = monkey._test(worry_level)
            monkeys[throw_target]._items.append(worry_level)
        inspections_this_round.append(len(monkey._items))
        monkey._items = []
    permutation = tuple(v._items for v in monkeys.values())
    if inspections_this_round in history_inspections_this_found:
        print(f"Repeat? round {round}")
        # break
    print(inspections_this_round)
    history_inspections_this_found.append(inspections_this_round)
    # print(permutation)
    # if permutation in permutations:
    #     print(f"Found a repeat permutation on round {round}")
    #     break
    # permutations.append(permutation)

    # print([v.inspections for v in monkeys.values()])
    # print(monkeys[0].inspections)

inspections = sorted([monkey.inspections for monkey in monkeys.values()], reverse=True)
monkey_business = inspections[0] * inspections[1]
print(f"Part 1: Monkey business is {monkey_business}")
