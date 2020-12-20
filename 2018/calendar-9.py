import llist
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
board = llist.dllist([0])
current_idx = 0
current_player = 0
print_board(board, current_idx, "-")

for i in range(1, LAST_MARBLE + 1):
	print(i)
	insertion_idx = (current_idx + 2) % len(board)
	if (i % 23) == 0:
		remove_idx = (current_idx - 7) % len(board)
		node = board.remove(board.nodeat(remove_idx))
		current_idx = remove_idx
		scores[current_player] += i + node
	elif insertion_idx == 0:
		board.append(i)
		current_idx = len(board) - 1
	else:
		board.insert(i, board.nodeat(insertion_idx))
		current_idx = insertion_idx
	# print_board(board, current_idx, current_player + 1)
	current_player = (current_player + 1) % PLAYERS

pprint.pprint(scores)
print(f"Part 1: highest score is {max(scores.values())}")

