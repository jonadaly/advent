from pathlib import Path

input_raw = Path("21-example.txt").read_text().strip().split("\n")


def practice_die():
    """Generator that yields 1-100 in order and then loops back to the start."""
    while True:
        yield from list(range(1, 101))


part1_die = practice_die()
p1_scores = [0]
p1_space = int(input_raw[0][-1])
p2_scores = [0]
p2_space = int(input_raw[1][-1])
total_rolls = 0
while True:
    print(f"Player 1: current space is {p1_space}, current score is {p1_scores[-1]}")
    print(f"Player 2: current space is {p2_space}, current score is {p2_scores[-1]}")
    p1_space += next(part1_die) + next(part1_die) + next(part1_die)
    p1_space = ((p1_space - 1) % 10) + 1
    total_rolls += 3

    print("end space", p1_space)
    p1_scores.append(p1_scores[-1] + p1_space)
    if p1_scores[-1] >= 1000:
        break

    p2_space += next(part1_die) + next(part1_die) + next(part1_die)
    p2_space = ((p2_space - 1) % 10) + 1
    total_rolls += 3

    print("end space", p2_space)
    p2_scores.append(p2_scores[-1] + p2_space)
    if p2_scores[-1] >= 1000:
        break


print(p1_scores, p2_scores)
print(f"Player 1 score {p1_scores[-1]}, player 2 score {p2_scores[-1]}")
print(f"Total rolls {total_rolls}")
print(f"part 1: product is {total_rolls*min(p1_scores[-1], p2_scores[-1])}")
