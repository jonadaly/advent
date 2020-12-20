import json
from collections import defaultdict
import pprint

with open("16.txt", "r") as f:
	raw_samples = f.read().split("\n\n")

def get_possible_codes(sample1):
	opc = sample1["op"][0]
	A = sample1["op"][1]
	B = sample1["op"][2]
	C = sample1["op"][3]

	possible_ops = []
	if sample1["before"][A] + sample1["before"][B] == sample1["after"][C]:
		possible_ops.append("addr")
	if sample1["before"][A] + B == sample1["after"][C]:
		possible_ops.append("addi")
	if sample1["before"][A] * sample1["before"][B] == sample1["after"][C]:
		possible_ops.append("mulr")
	if sample1["before"][A] * B == sample1["after"][C]:
		possible_ops.append("muli")
	if sample1["before"][A] & sample1["before"][B] == sample1["after"][C]:
		possible_ops.append("banr")
	if sample1["before"][A] & B == sample1["after"][C]:
		possible_ops.append("bani")
	if sample1["before"][A] | sample1["before"][B] == sample1["after"][C]:
		possible_ops.append("borr")
	if sample1["before"][A] | B == sample1["after"][C]:
		possible_ops.append("bori")
	if sample1["before"][A] == sample1["after"][C]:
		possible_ops.append("setr")
	if A == sample1["after"][C]:
		possible_ops.append("seti")
	if A > sample1["before"][B] and sample1["after"][C] == 1 or A <= sample1["before"][B] and sample1["after"][C] == 0:
		possible_ops.append("gtir")
	if sample1["before"][A] > B and sample1["after"][C] == 1 or sample1["before"][A] <= B and sample1["after"][C] == 0:
		possible_ops.append("gtri")
	if sample1["before"][A] > sample1["before"][B] and sample1["after"][C] == 1 or sample1["before"][A] <= sample1["before"][B] and sample1["after"][C] == 0:
		possible_ops.append("gtrr")
	if A == sample1["before"][B] and sample1["after"][C] == 1 or A != sample1["before"][B] and sample1["after"][C] == 0:
		possible_ops.append("eqir")
	if sample1["before"][A] == B and sample1["after"][C] == 1 or sample1["before"][A] != B and sample1["after"][C] == 0:
		possible_ops.append("eqri")
	if sample1["before"][A] == sample1["before"][B] and sample1["after"][C] == 1 or sample1["before"][A] != sample1["before"][B] and sample1["after"][C] == 0:
		possible_ops.append("eqrr")
	return opc, possible_ops

# Parse input
program = raw_samples[-1]
samples = []
for raw_s in raw_samples[:-2]:
	lines = raw_s.split("\n")
	samples.append({
		"before": json.loads(lines[0].split(":")[1]),
		"op": [int(x) for x in lines[1].split()],
		"after": json.loads(lines[2].split(":")[1])
	})

# Part 1: figure out what samples have 3 or more possible op codes.
count = 0
op_codes = {}
for i, s in enumerate(samples):
	op_code, possible_ops = get_possible_codes(s)
	# print(f"sample: {i}, num possible_ops: {len(possible_ops)}")
	if len(possible_ops) >= 3:
		count += 1
	if op_code not in op_codes:
		# Init the list.
		op_codes[op_code] = possible_ops
	else:
		# Append unique values to the list.
		op_codes[op_code] = list(set(op_codes[op_code]).intersection(set(possible_ops)))

print(f"Part 1: {count} samples behave like 3 or more possible op codes")

# We now have a set of possibilities for each op code. Work out which is which!
final_op_codes = {}
while True:
	chosen_op_code = None
	chosen_operation = None
	for op_code, possible_ops in op_codes.items():
		if len(possible_ops) == 1:
			chosen_op_code = op_code
			chosen_operation = possible_ops[0]
			break

	if chosen_op_code is None:
		raise ValueError("We got stuck :(")

	# Add identified op code / operation pair to the final list
	final_op_codes[chosen_op_code] = chosen_operation
	del op_codes[chosen_op_code]

	# Break from the loop if we're done. 
	if len(op_codes) == 0:
		break

	# Remove the assigned operation from the lists of possibilities.
	for op_code, possible_ops in op_codes.items():
		op_codes[op_code] = [o for o in possible_ops if o != chosen_operation]

print("Final op codes:")
pprint.pprint(final_op_codes)

# Part 2: Run the test program
registers = [0, 0, 0, 0]
for line in program.strip().split("\n"):
	opc = int(line.split()[0].strip())
	A = int(line.split()[1].strip())
	B = int(line.split()[2].strip())
	C = int(line.split()[3].strip())
	operation = final_op_codes[opc]
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

print(f"Part 2: After executing program, register 0 is {registers[0]}")
