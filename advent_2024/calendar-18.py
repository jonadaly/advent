from collections import deque
from pathlib import Path


raw_input = Path("18.txt").read_text().strip().split("\n")
byte_positions = [
    complex(int(line.split(",")[0]), int(line.split(",")[1])) for line in raw_input
]
SIZE = 71
BYTES_PART1 = 1024


def bfs(
    start: complex, end: complex, byte_positions: list[complex]
) -> list[complex] | None:
    queue = deque([start])
    visited = {start}
    parents = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            # reconstruct the path
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]
        for direction in [-1, 1, -1j, 1j]:
            new_pos = current + direction
            if (
                new_pos in visited  # we've been here before
                or new_pos in byte_positions  # blocked by a byte
                or new_pos.real < 0  # out of bounds
                or new_pos.imag < 0
                or new_pos.real >= SIZE
                or new_pos.imag >= SIZE
            ):
                continue
            visited.add(new_pos)
            parents[new_pos] = current
            queue.append(new_pos)
    return None


p1_path = bfs(0j, complex(SIZE - 1, SIZE - 1), byte_positions[:BYTES_PART1])
print(f"Part 1: length is {len(p1_path)}")

# Binary search is way faster than iterating.
start = 1
end = len(byte_positions) - 1
while True:
    mid = (start + end) // 2
    path = bfs(0j, complex(SIZE - 1, SIZE - 1), byte_positions[:mid])
    if path:
        start = mid + 1
    else:
        end = mid
    if start == end:
        last_byte = byte_positions[start - 1]
        print(
            f"Part 2: no path after byte ({int(last_byte.real)},{int(last_byte.imag)}) has fallen"
        )
        break
