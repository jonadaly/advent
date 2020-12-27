from pathlib import Path
from typing import List, Tuple, Dict, Set
import re
from collections import deque
import hashlib
from itertools import chain
import math
import matplotlib.pyplot as plt

raw_lines = Path("25.txt").read_text().strip().split("\n")
card_public_key = int(raw_lines[0])
door_public_key = int(raw_lines[1])
PK_SUBJECT_NUMBER = 7
DIVISOR = 20201227

card_loop_number = card_value = door_loop_number = door_value = encryption_key = 1
while (card_value := (card_value * PK_SUBJECT_NUMBER) % DIVISOR) != card_public_key:
    card_loop_number += 1
while (door_value := (door_value * PK_SUBJECT_NUMBER) % DIVISOR) != door_public_key:
    door_loop_number += 1
for i in range(card_loop_number):
    encryption_key = (encryption_key * door_public_key) % DIVISOR

print(f"Part 1: encryption key is {encryption_key}")
