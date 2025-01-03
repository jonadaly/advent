import operator
from pathlib import Path
import re


raw_inputs, raw_gates = Path("24.txt").read_text().strip().split("\n\n")
wires: dict[str, int] = {
    r.split(": ")[0]: int(r.split(": ")[1]) for r in raw_inputs.split("\n")
}
gates: list[tuple[str, ...]] = [
    re.match(r"(.+) (.+) (.+) -> (.+)", gate).groups() for gate in raw_gates.split("\n")
]

OPERATORS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}

while True:
    initial_state = wires.copy()
    for input1, op, input2, output in gates:
        if input1 not in wires or input2 not in wires:
            continue
        wires[output] = OPERATORS[op](wires[input1], wires[input2])
    if wires == initial_state:
        break


def get_integer(label: str) -> int:
    outputs = {k: v for k, v in wires.items() if v.startswith(label)}
    return int(
        "".join(str(outputs[k]) for k in sorted(outputs.keys(), reverse=True)), 2
    )


print(f"Part 1: Z value is {get_integer("z")}")

z_msb_label = sorted({output for output in wires.keys() if output.startswith("z")})[-1]


# This looks like a ripple carry adder: https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder
# So there are some rules!
def is_valid_gate(gate: tuple[str, ...]) -> bool:
    input1, op, input2, output = gate
    # 1) Gates outputting a bit of Z must be XOR, except for the MSB which must be OR
    if output[0] == "z":
        if output == z_msb_label and op != "OR":
            return False
        if output != z_msb_label and op != "XOR":
            return False
    # 2) XOR gates that don't have X or Y bits as inputs must output bits of Z
    if (
        op == "XOR"
        and input1[0] not in ["x", "y"]
        and input2[0] not in ["x", "y"]
        and output[0] != "z"
    ):
        return False
    # 3) AND gates must have an output that is an input to an OR gate, except for the half-adder at the start
    if (
        op == "AND"
        and "x00" not in [input1, input2]
        and any(
            (output == other_input1 or output == other_input2) and other_op != "OR"
            for other_input1, other_op, other_input2, _ in gates
        )
    ):
        return False
    # 4) XOR gates must not have an output that is an input to an OR gate
    if op == "XOR" and any(
        (output == other_input1 or output == other_input2) and other_op == "OR"
        for other_input1, other_op, other_input2, _ in gates
    ):
        return False
    return True


swapped = {g[3] for g in gates if not is_valid_gate(g)}
print(f"Part 2: following wires are swapped: {",".join(sorted(list(swapped)))}")
