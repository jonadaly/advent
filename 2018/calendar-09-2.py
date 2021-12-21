from collections import deque
import pprint

PLAYERS = 430
LAST_MARBLE = 7158800

def print_board(board, current_idx, current_player):
	line = f"[{current_player}] "
	for i in range(len(board)):
		if i == current_idx:
			line += f"({board[i]}) "
		else:
			line += f" {board[i]} "
	print(line)

scores = {p: 0 for p in range(PLAYERS)}
board = deque([0])
current_idx = 0
current_player = 0
print_board(board, current_idx, "-")

for i in range(1, LAST_MARBLE + 1):
	if (i % 23) == 0:
		board.rotate(7)
		scores[current_player] += i + board.pop()
		board.rotate(-1)
	else:
		board.rotate(-1)
		board.append(i)
	current_player = (current_player + 1) % PLAYERS

pprint.pprint(scores)
print(f"Part 1: highest score is {max(scores.values())}")

