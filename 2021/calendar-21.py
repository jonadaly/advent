from functools import lru_cache
from pathlib import Path
from typing import Tuple

input_raw = Path("21.txt").read_text().strip().split("\n")


### Part 1 ###


def practice_die():
    """Generator that yields 1-100 in order and then loops back to the start."""
    while True:
        yield from list(range(1, 101))


part1_die = practice_die()
p1_space = int(input_raw[0][-1])
p1_score = 0
p2_space = int(input_raw[1][-1])
p2_score = 0
total_rolls = 0
while True:
    p1_space += next(part1_die) + next(part1_die) + next(part1_die)
    p1_space = ((p1_space - 1) % 10) + 1
    total_rolls += 3
    p1_score += p1_space
    if p1_score >= 1000:
        break

    p2_space += next(part1_die) + next(part1_die) + next(part1_die)
    p2_space = ((p2_space - 1) % 10) + 1
    total_rolls += 3
    p2_score += p2_space
    if p2_score >= 1000:
        break

print(f"Part 1: product is {total_rolls*min(p1_score, p2_score)}")


### Part 2 ###


# Frequency of possible sums of three dice rolls.
POSSIBILITIES = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@lru_cache(maxsize=None)
def play_game_from(
    _p1_space: int,
    _p2_space: int,
    _p1_score: int,
    _p2_score: int,
    is_player_1_turn: bool,
) -> Tuple[int, int]:
    """
    Recursive function that calculates the number of wins given a starting state (position/score for each player,
    as well as whose turn it is). Makes use of a cache so as to not repeat work. Returns the number of possible
    wins for each player from that starting state.
    """
    if _p1_score >= 21:
        return 1, 0
    if _p2_score >= 21:
        return 0, 1

    # Need a running total of all possible winners from this state.
    ovr_p1_wins = 0
    ovr_p2_wins = 0

    # Loop through each roll possibility, calculate the resulting state and the number of wins from that state.
    for roll_total, freq in POSSIBILITIES.items():
        new_p1_space = _p1_space
        new_p1_score = _p1_score
        new_p2_space = _p2_space
        new_p2_score = _p2_score
        # Update state.
        if is_player_1_turn:
            new_p1_space = ((_p1_space + roll_total - 1) % 10) + 1
            new_p1_score = _p1_score + new_p1_space
        else:
            new_p2_space = ((_p2_space + roll_total - 1) % 10) + 1
            new_p2_score = _p2_score + new_p2_space
        # Calculate wins from new state.
        _p1_wins, _p2_wins = play_game_from(
            _p1_space=new_p1_space,
            _p2_space=new_p2_space,
            _p1_score=new_p1_score,
            _p2_score=new_p2_score,
            is_player_1_turn=(not is_player_1_turn),
        )
        ovr_p1_wins += freq * _p1_wins
        ovr_p2_wins += freq * _p2_wins

    return ovr_p1_wins, ovr_p2_wins


p1_wins, p2_wins = play_game_from(
    _p1_space=int(input_raw[0][-1]),
    _p2_space=int(input_raw[1][-1]),
    _p1_score=0,
    _p2_score=0,
    is_player_1_turn=True,
)
print(f"Part 2: the winning player wins in {max(p1_wins, p2_wins)} universes")
