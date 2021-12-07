from collections import defaultdict
from pathlib import Path

import numpy as np

bingo_raw = Path("4.txt").read_text().strip()
draw_numbers_raw, boards_raw = bingo_raw.split("\n", 1)
draw_numbers = draw_numbers_raw.strip().split(",")

combinations = defaultdict(list)
for i_board, board_raw in enumerate(boards_raw.split("\n\n")):
    board = np.array([row.strip().split() for row in board_raw.strip().split("\n")])
    for row in board:
        combinations[i_board].append(row.tolist())
    for col in board.transpose():
        combinations[i_board].append(col.tolist())

finishing_scores = {}
for draw_number in draw_numbers:
    for i_board, board_combinations in combinations.items():
        if i_board in finishing_scores:
            continue
        finished = False
        for combination in board_combinations:
            if draw_number in combination:
                del combination[combination.index(draw_number)]
                if len(combination) == 0:
                    finished = True
        if finished:
            total = sum({int(x) for y in board_combinations for x in y})
            score = int(draw_number) * total
            print(
                f"Board {i_board} complete after number {draw_number} - score {score}"
            )
            finishing_scores[i_board] = score

print(
    f"Part 1: winning board is board {list(finishing_scores.keys())[0]} with a score of {list(finishing_scores.values())[0]}"
)
print(
    f"Part 1: losing board is board {list(finishing_scores.keys())[-1]} with a score of {list(finishing_scores.values())[-1]}"
)
