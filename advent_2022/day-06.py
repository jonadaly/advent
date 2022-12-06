from collections import deque
from pathlib import Path

signal: str = Path("day-06-input.txt").read_text().strip()


def search(signal: str, *, length: int) -> int:
    queue = deque(signal[:length])
    for i in range(length, len(signal)):
        if len(set(queue)) == length:
            return i
        queue.popleft()
        queue.append(signal[i])
    raise Exception


print(f"Part 1: found signal after {search(signal, length=4)} chars")
print(f"Part 2: found signal after {search(signal, length=14)} chars")
