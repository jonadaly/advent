import pprint

with open("21.txt", "r") as f:
    raw_instructions = f.readlines()


def run_instruction(instruction: dict):
    A = instruction["A"]
    B = instruction["B"]
    C = instruction["C"]
    operation = instruction["op"]
    if operation == "addr":
        registers[C] = registers[A] + registers[B]
    elif operation == "addi":
        registers[C] = registers[A] + B
    elif operation == "mulr":
        registers[C] = registers[A] * registers[B]
    elif operation == "muli":
        registers[C] = registers[A] * B
    elif operation == "banr":
        registers[C] = registers[A] & registers[B]
    elif operation == "bani":
        registers[C] = registers[A] & B
    elif operation == "borr":
        registers[C] = registers[A] | registers[B]
    elif operation == "bori":
        registers[C] = registers[A] | B
    elif operation == "setr":
        registers[C] = registers[A]
    elif operation == "seti":
        registers[C] = A
    elif operation == "gtir":
        registers[C] = 1 if A > registers[B] else 0
    elif operation == "gtri":
        registers[C] = 1 if registers[A] > B else 0
    elif operation == "gtrr":
        registers[C] = 1 if registers[A] > registers[B] else 0
    elif operation == "eqir":
        registers[C] = 1 if A == registers[B] else 0
    elif operation == "eqri":
        registers[C] = 1 if registers[A] == B else 0
    elif operation == "eqrr":
        registers[C] = 1 if registers[A] == registers[B] else 0
    else:
        raise ValueError


instructions = []
for line in raw_instructions:
    if line.startswith("#ip"):
        instruction_register = int(line.split()[1].strip())
        continue
    op = line.split()[0].strip()
    A = int(line.split()[1].strip())
    B = int(line.split()[2].strip())
    C = int(line.split()[3].strip())
    instructions.append(
        {
            "op": op,
            "A": A,
            "B": B,
            "C": C,
        }
    )

print(f"instruction_register: {instruction_register}")
pprint.pprint(instructions)

registers = [0, 0, 0, 0, 0, 0]
history_reg_4_at_28 = []
while True:
    state_before_str = f"ip={registers[instruction_register]} {registers}"
    instruction_pointer = registers[instruction_register]
    current_instruction = instructions[instruction_pointer]
    run_instruction(current_instruction)
    # print(f"{state_before_str} {list(current_instruction.values())} {registers}")
    if registers[instruction_register] == 28:
        if registers[4] in history_reg_4_at_28:
            print(f"FOUND REPEAT VALUE {registers[4]}")
            # We are repeating - break here.
            break
        history_reg_4_at_28.append(registers[4])
        print(registers[4])
    registers[instruction_register] = registers[instruction_register] + 1

# #ip 2
# seti 123 0 4        r4 = 123
# bani 4 456 4        r4 = r4 & 456
# eqri 4 72 4         r4 = r4 == 72
# addr 4 2 2          jumprel by r4
# seti 0 0 2          jumpabs to beginning
# seti 0 5 4          r4 = 0
# bori 4 65536 5      r5 = r4 | 65536
# seti 1765573 9 4    r4 = 1765573
# bani 5 255 1        r1 = r5 & 255
# addr 4 1 4          r4 = r1 + r4
# bani 4 16777215 4   r4 = r4 & 16777215
# muli 4 65899 4      r4 = r4 * 65899
# bani 4 16777215 4   r4 = r4 & 16777215
# gtir 256 5 1        r1 = 256 > r5
# addr 1 2 2          jumprel by r1
# addi 2 1 2          jumprel by 1
# seti 27 0 2         jumpabs to 27
# seti 0 8 1          r1 = 0
# addi 1 1 3          r3 = r1 + 1
# muli 3 256 3        r3 = r3 * 256
# gtrr 3 5 3          r3 = r3 > r5
# addr 3 2 2          jumprel by r3
# addi 2 1 2          jumprel by 1
# seti 25 1 2         jumpabs to 25
# addi 1 1 1          r1 = r1 + 1
# seti 17 7 2         r2 = 17
# setr 1 4 5          r5 = r1
# seti 7 6 2          jumpabs to 7
# eqrr 4 0 1          r1 = r4 == r0
# addr 1 2 2          jumprel by r1
# seti 5 2 2          jumpabs to 5

# Program halts (during instruction 28) only if r4 value equals r0 value (which is constant). So only way to exit
# program is to initialise r0 to a given value

# Part 1: Halts if r4 matches the starting value. So figure out what the value of r4 is the first time we get to
# instruction 28.
print(f"Part 1: {history_reg_4_at_28[0]}")

# Part 2: Loop until we get a repeating pattern in register 4 for instruction 28. The last value in the pattern is the answer.
print(f"Part 1: {history_reg_4_at_28[-1]}")
