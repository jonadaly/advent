from pathlib import Path


# Parse input
raw_input = Path("17.txt").read_text().strip().split("\n")
A = int(raw_input[0].split(": ")[1])
B = int(raw_input[1].split(": ")[1])
C = int(raw_input[2].split(": ")[1])
program = list(map(int, raw_input[4].split(": ")[1].split(",")))


# Part 1 - run program.
pointer = 0
output = []
while True:
    if pointer >= len(program):
        break
    instruction = program[pointer]
    operand = program[pointer + 1]
    # print(f"{pointer=}, {instruction=}, {operand=}")
    combo = {0: 0, 1: 1, 2: 2, 3: 3, 4: A, 5: B, 6: C}
    match instruction, operand:
        case 0, op: A = int(A/(2**combo[op]))
        case 1, op: B = B ^ op
        case 2, op: B = combo[op] % 8
        case 3, op: pointer = op-2 if A != 0 else pointer
        case 4, op: B = B ^ combo[op]
        case 5, op: output.append(combo[op] % 8)
        case 6, op: B = int(A/(2**combo[op]))
        case 7, op: C = int(A/(2**combo[op]))
    pointer += 2

print(f"Part 1: output is {",".join(str(o) for o in output)}")

# Part 2: Brute forcing would take too long, so we need to work backwards from the desired output to find
# the value of A.


# We can reverse engineer the instructions into the following loop. Note the instruction A = A >> B, which doesn't do
# anything in terms of the output - but since B is always 3 it means we're always dividing A by 8 each loop.
def loop(A: int) -> int:
    B = A % 8
    B = B ^ 5
    C = A >> B
    A = A >> B
    B = B ^ C
    B = B ^ 6
    return B % 8


def check(A: int, index: int) -> int | None:
    if loop(A) != program[-(index + 1)]:
        # Then this A can't be correct as it doesn't produce the output we need.
        return None
    if index == len(program) - 1:
        # Then we're found the correct value of A that produces the output we need.
        return A
    # Our A so far is right, so we need to reverse the "dividing by 8" step above, and try an offset
    for next in range(8):
        updated_A = A * 8 + next
        candidate = check(updated_A, index=index + 1)
        if candidate is not None:
            return candidate
    return None


# We only need to search up to 8 because the first step of the loop is always % 8
for A in range(8):
    candidate = check(A, index=0)
    if candidate:
        print(f"Part 2: lowest is {candidate}")
        break
