import json
from collections import defaultdict
import pprint

with open("19.txt", "r") as f:
	raw_instructions = f.readlines()

# raw_instructions = """#ip 0
# seti 5 0 1
# seti 6 0 2
# addi 0 1 0
# addr 1 2 3
# setr 1 0 0
# seti 8 0 4
# seti 9 0 5""".split("\n")

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
	instructions.append({
		"op": op,
		"A": A,
		"B": B,
		"C": C,
		})

import pprint
print(f"instruction_register: {instruction_register}")
pprint.pprint(instructions)

# registers = [0, 0, 0, 0, 0, 0]
# while True:
# 	if (registers[instruction_register] >= len(instructions)):
# 		print(f"Part 1 done: Final registers {registers}")
# 		break
# 	state_before_str = f"ip={registers[instruction_register]} {registers}"
# 	instruction_pointer = registers[instruction_register]
# 	current_instruction = instructions[instruction_pointer]		
# 	run_instruction(current_instruction)
# 	print(f"{state_before_str} {list(current_instruction.values())} {registers}")
# 	registers[instruction_register] = registers[instruction_register] + 1

registers = [1, 0, 0, 0, 0, 0]
for i in range(200):
	if (registers[instruction_register] >= len(instructions)):
		print(f"Part 1 done: Final registers {registers}")
		break
	state_before_str = f"ip={registers[instruction_register]} {registers}"
	instruction_pointer = registers[instruction_register]
	current_instruction = instructions[instruction_pointer]		
	run_instruction(current_instruction)
	print(f"{state_before_str} {list(current_instruction.values())} {registers}")
	registers[instruction_register] = registers[instruction_register] + 1

# After a few iterations, this loops a lot
# ip=3  ['mulr', 1, 2, 3] is equivalent to r3 = r1*r2
# ip=4  ['eqrr', 3, 5, 3] is equivalent to r3 = r3 == r5
# ip=5  ['addr', 3, 4, 4] is equivalent to RELJUMP by r3
# ip=6  ['addi', 4, 1, 4] is equivalent to RELJUMP by 1
# ip=8  ['addi', 2, 1, 2] is equivalent to r2 = r2 + 1
# ip=9  ['gtrr', 2, 5, 3] is equivalent to r3 = r2 > r5
# ip=10 ['addr', 4, 3, 4] is equivalent to RELJUMP by r3
# ip=11 ['seti', 2, 7, 4] is equivalent to ABSJUMP to 2

# Occasionally this little loop runs
# ip=12 ['addi', 1, 1, 1] is equivalent to r1 = r1 + 1
# ip=13 ['gtrr', 1, 5, 3] is equivalent to r3 = r1 > r5
# ip=14 ['addr', 3, 4, 4] is equivalent to reljump by r3
# ip=15 ['seti', 1, 9, 4] is equivalent to absjump to 1
# ip=2  ['seti', 1, 2, 2] is equivalent to r2 = 1

# # PART 1 equivalent:
# r0 = 0
# r1 = 1
# r2 = 1
# r3 = 40
# r4 = 3
# r5 = 876

# PART 2 equivalent:
r0 = 0
r1 = 1
r2 = 0
r3 = 10550400
r4 = 2
r5 = 10551276
while True:
	r2 += 1
	if r2 > r5:
		r1 += 1
		if r1 > r5:
			break
		else:
			r2 = 1

	if r2*r1 == r5:
		r0 += r1
		print(r0)

	# Skip ahead if possible - it would just increment by one normally and that would take ages
	if r2 > r5/r1:
		r2 = r5	
	
print(f"Final value: {r0}")


