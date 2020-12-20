from pathlib import Path
import numpy as np
from typing import Dict, Tuple, List
import re


equations = Path("18.txt").read_text().strip().split("\n")


def evaluate(equation, part2):
    latest_equation = equation
    while "(" in latest_equation:
        i_start = latest_equation.find("(")
        nesting = 0
        for ichar, char in enumerate(latest_equation[i_start:]):
            if char == "(":
                nesting += 1
            elif char == ")":
                nesting -= 1
            if nesting == 0:
                i_end = ichar + i_start
                break
        inner = latest_equation[i_start+1:i_end]
        result = evaluate(inner, part2)
        latest_equation = latest_equation.replace(f"({inner})", result, 1)
    # No brackets left.

    while part2 and "+" in latest_equation:
        groups = re.search(r"(\d+) \+ (\d+)", latest_equation).groups()
        operand1 = int(groups[0])
        operand2 = int(groups[1])
        result = operand1 + operand2
        latest_equation = latest_equation.replace(f"{operand1} + {operand2}", str(result), 1)

    while " " in latest_equation:
        groups = re.match(r"(\d+) ([+\-\*]) (\d+)", latest_equation).groups()
        operand1 = int(groups[0])
        operator = groups[1]
        operand2 = int(groups[2])
        if operator == "+":
            result = operand1 + operand2
        elif operator == "*":
            result = operand1 * operand2
        else:
            raise NotImplemented
        latest_equation = latest_equation.replace(f"{operand1} {operator} {operand2}", str(result), 1)
    return latest_equation


sum = 0
results = []
for equation in equations:
    result = evaluate(equation, part2=False)
    results.append(int(result))
    sum += int(result)
print(f"Part 1: total is {sum}")

sum = 0
results = []
for equation in equations:
    result = evaluate(equation, part2=True)
    results.append(int(result))
    sum += int(result)
print(f"Part 2: total is {sum}")