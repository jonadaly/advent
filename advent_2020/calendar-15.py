from collections import defaultdict

starting_numbers = [1, 12, 0, 20, 8, 16]
numbers = defaultdict(list)
for k, v in enumerate(starting_numbers):
    numbers[v].append(k + 1)

# END_TURN = 2020 # Part 1
END_TURN = 30000000  # Part 2 - takes a minute
turn = len(starting_numbers) + 1
last_number = starting_numbers[-1]
while turn <= END_TURN:
    history = numbers[last_number]
    if len(history) > 1:
        new_number = history[-1] - history[-2]
    else:
        new_number = 0
    numbers[new_number].append(turn)
    last_number = new_number
    turn += 1
# print(f"Part 1: 2020th turn is {last_number}")
print(f"Part 2: 30000000th turn is {last_number}")
