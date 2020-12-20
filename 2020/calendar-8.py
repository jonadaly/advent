from pathlib import Path
import re

instructions = Path("8.txt").read_text().strip().split("\n")

def execute(instructions):
    accum = 0
    pointer = 0
    executed = set()
    looping = False
    while True:
        if pointer >= len(instructions):
            looping = False
            break
        if pointer in executed:
            looping = True
            break
        executed.add(pointer)
        instruction = instructions[pointer]
        if instruction.startswith("acc"):
            accum += int(instruction[4:])
        elif instruction.startswith("jmp"):
            pointer += int(instruction[4:]) - 1
        pointer += 1
    return accum, looping

# Part 1
accum, looping = execute(instructions)
assert looping is True
print(f"Part 1: accumulator contains {accum}")

# Part 2
for i, instruction in enumerate(instructions):
    print(f"Trying to mutate line {i}")
    mutated_instructions = instructions.copy()
    if instruction[:3] == "acc":
        continue
    elif instruction[:3] == "nop":
        mutated_instructions[i] = instruction.replace("nop", "jmp")
    elif instruction[:3] == "jmp":
        mutated_instructions[i] = instruction.replace("jmp", "nop")
    accum, looping = execute(mutated_instructions)
    if looping is False:
        break
print(f"Part 2: accumulator contains {accum}")
    
    