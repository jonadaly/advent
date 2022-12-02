import hashlib
from collections import deque
from pathlib import Path

raw_deck_1, raw_deck_2 = Path("22.txt").read_text().strip().split("\n\n")
deck_1 = deque(map(int, raw_deck_1.split("\n")[1:]))
deck_2 = deque(map(int, raw_deck_2.split("\n")[1:]))

# Part 1
while len(deck_1) > 0 and len(deck_2) > 0:
    card_1 = deck_1.popleft()
    card_2 = deck_2.popleft()
    if card_1 > card_2:
        deck_1.append(card_1)
        deck_1.append(card_2)
    else:
        deck_2.append(card_2)
        deck_2.append(card_1)
winning_deck = deck_1 if len(deck_1) > 0 else deck_2
winning_deck.reverse()
total_score = sum(c * (i + 1) for i, c in enumerate(winning_deck))
print(f"Part 1: total score is {total_score}")

# Part 2
deck_1 = deque(map(int, raw_deck_1.split("\n")[1:]))
deck_2 = deque(map(int, raw_deck_2.split("\n")[1:]))


def recursive_combat(deck_1, deck_2) -> int:
    round_hashes = set()
    iround = 1
    while len(deck_1) > 0 and len(deck_2) > 0:
        # print(f"Round {iround}")
        # print(f"Player 1: {deck_1}")
        # print(f"Player 2: {deck_2}")
        round_hash = hashlib.md5(bytes(deck_1) + b"|" + bytes(deck_2)).hexdigest()
        if round_hash in round_hashes:
            # print("STOP - infinite loop")
            return 1
        round_hashes.add(round_hash)
        card_1 = deck_1.popleft()
        card_2 = deck_2.popleft()
        if card_1 <= len(deck_1) and card_2 <= len(deck_2):
            # print("RECURSE")
            sub_deck_1 = deque(list(deck_1)[:card_1])
            sub_deck_2 = deque(list(deck_2)[:card_2])
            winner = recursive_combat(sub_deck_1, sub_deck_2)
            # print("END RECURSE")
        else:
            # print("NORMAL")
            winner = 1 if card_1 > card_2 else 2
        # print("WINNER: " + str(winner))
        if winner == 1:
            deck_1.append(card_1)
            deck_1.append(card_2)
        else:
            deck_2.append(card_2)
            deck_2.append(card_1)
        iround += 1
    return 1 if len(deck_1) > 0 else 2


TIMES_CALLED = 0
result = recursive_combat(deck_1, deck_2)
# print("FINAL DECKS: ", deck_1, deck_2)
winning_deck = deck_1 if len(deck_1) > 0 else deck_2
winning_deck.reverse()
total_score = sum(c * (i + 1) for i, c in enumerate(winning_deck))
print(f"Part 2: total score is {total_score}")
