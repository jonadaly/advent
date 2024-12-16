from enum import Enum
import heapq
from pathlib import Path


raw_input = Path("16.txt").read_text().strip().split("\n")
map = [list(line) for line in raw_input]


class MyComplex(complex):
    """Custom class because heapq tries to compare complex numbers when there's a tie in score tie."""

    def __lt__(self, other):
        return (self.imag, self.real) < (other.imag, other.real)

    def __add__(self, other):
        return MyComplex(complex(self) + other)


class Face(Enum):
    NORTH = MyComplex(-1, 0)
    EAST = MyComplex(0, 1)
    SOUTH = MyComplex(1, 0)
    WEST = MyComplex(0, -1)


START = MyComplex(len(map) - 2, 1)
END = MyComplex(1, len(map[0]) - 2)

# Need dijkstra rather than bfs because of cost of turning - hence priority queue.
visited: dict[tuple[MyComplex, MyComplex], int] = {}
queue = [(0, START, Face.EAST.value, [START])]  # score, position, direction, path
best = float("inf")
locs_on_best_path: set[MyComplex] = set()
while queue:
    cost, pos, face, path = heapq.heappop(queue)
    if cost > best:
        # We're already worse than the best route - abort.
        break
    visited[pos, face] = cost
    if pos == END:
        if cost < best:
            locs_on_best_path.clear()
        best = cost
        locs_on_best_path |= set(path)
    for new_face in Face:
        new_pos = pos + new_face.value
        step_cost = 1 if new_face.value == face else 1001
        if map[int(new_pos.real)][int(new_pos.imag)] == "#":
            # Can't go this way - dead end.
            continue
        if visited.get((new_pos, new_face.value), float("inf")) > cost + step_cost:
            # We're better than the current best - continue searching.
            heapq.heappush(
                queue, (cost + step_cost, new_pos, new_face.value, path + [new_pos])
            )

print(f"Part 1: best score is {best}")
print(f"Part 2: {len(locs_on_best_path)} seats on best paths")
