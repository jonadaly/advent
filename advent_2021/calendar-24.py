from collections import defaultdict, deque
from pathlib import Path

instructions_raw = Path("24.txt").read_text().strip().split("\n")

instructions = []
for instruction_raw in instructions_raw:
    operator, *args = instruction_raw.split()
    instructions.append((operator, args))


class Variables:
    w = 0
    x = 0
    y = 0
    z = 0

    def __repr__(self):
        return f"w: {self.w}, x: {self.x}, y: {self.y}, z: {self.z}"


def run_program(_inputs: deque) -> Variables:
    _variables = Variables()
    for operator, args in instructions:
        if operator == "inp":
            setattr(_variables, args[0], int(_inputs.popleft()))
            continue
        arg1 = getattr(_variables, args[0])
        arg2 = (
            int(args[1])
            if args[1].lstrip("-").isnumeric()
            else getattr(_variables, args[1])
        )
        if operator == "add":
            setattr(_variables, args[0], arg1 + arg2)
        elif operator == "mul":
            setattr(_variables, args[0], arg1 * arg2)
        elif operator == "div":
            setattr(_variables, args[0], arg1 // arg2)
        elif operator == "mod":
            setattr(_variables, args[0], arg1 % arg2)
        elif operator == "eql":
            setattr(_variables, args[0], 1 if arg1 == arg2 else 0)
        else:
            raise ValueError
    return _variables


# # JK, this would take until the heat death of the universe.
# times = 0
# valid = []
# serial = 99999999999999
# while True:
#     i_str = str(serial).zfill(14)
#     if "0" not in i_str:
#         inputs = deque(list(i_str))
#         variables = run_program(inputs)
#         if str(variables.z).startswith("28040"):
#             print(f"Interesting: {i_str} is {variables.z}")
#         if variables.z == 0:
#             valid.append(i_str)
#             break
#     serial -= 1


# Another approach: decompile the source and simplify.
def f(w: int, z: int, a: int, b: int, c: int):
    if (z % 26) + a == w:
        return z // c
    else:
        return (z // c) * 26 + w + b


# What's the equivalent of f in reverse?
def f_reverse(w, z_after, a, b, c) -> list:
    possible_z = []
    x = z_after - w - c
    if x % 26 == 0:
        possible_z.append(x // 26 * a)
    if 0 <= w - b < 26:
        possible_z.append(w - b + (z_after * a))
    return possible_z


# Pulled these out of the inputs - they are the only values that differ in the sets of 18 instructions.
a_values = [1, 1, 1, 1, 26, 1, 26, 1, 1, 26, 26, 26, 26, 26]
b_values = [11, 14, 15, 13, -12, 10, -15, 13, 10, -13, -13, -14, -2, -9]
c_values = [14, 6, 6, 13, 8, 8, 7, 10, 8, 12, 10, 8, 8, 7]


def solve(w_range):
    z_targets = {0}
    serials = defaultdict(list)
    for i in reversed(range(len(b_values))):
        z_targets_new = set()
        for w in w_range:
            for zt in z_targets:
                z_possibilities = f_reverse(
                    w, zt, a_values[i], b_values[i], c_values[i]
                )
                for zp in z_possibilities:
                    z_targets_new.add(zp)
                    # Overwrite as new results will always be more complete / higher in value.
                    serials[zp] = [
                        w,
                        *serials[zt],
                    ]
        z_targets = z_targets_new
    # We always start with z=0, so choose the serial with that starting value.
    return "".join(str(d) for d in serials[0])


print(f"Part 1: {solve(range(1, 10))} is highest valid serial")
print(f"Part 2: {solve(range(9, 0, -1))} is lowest valid serial")
