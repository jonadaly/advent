from pathlib import Path

instructions: list[str] = Path("day-09-input.txt").read_text().strip().split("\n")


def move(start: tuple[int, int], vector: tuple[int, int]) -> tuple[int, int]:
    return (start[0] + vector[0], start[1] + vector[1])


def track_tail(knots: int) -> set[tuple[int, int]]:
    visited: set[tuple[int, int]] = {(0, 0)}
    pos = [(0, 0) for _ in range(knots)]
    for instruction in instructions:
        direction, amount = instruction.split(" ")
        for _ in range(int(amount)):
            match (direction):
                case "R":
                    pos[0] = move(pos[0], (1, 0))
                case "L":
                    pos[0] = move(pos[0], (-1, 0))
                case "U":
                    pos[0] = move(pos[0], (0, 1))
                case "D":
                    pos[0] = move(pos[0], (0, -1))
            # Update tail
            for i in range(1, knots):
                diff = (pos[i - 1][0] - pos[i][0], pos[i - 1][1] - pos[i][1])
                match (diff):
                    case (2, 0):
                        pos[i] = move(pos[i], (1, 0))
                    case (-2, 0):
                        pos[i] = move(pos[i], (-1, 0))
                    case (0, 2):
                        pos[i] = move(pos[i], (0, 1))
                    case (0, -2):
                        pos[i] = move(pos[i], (0, -1))
                    case (1, 2) | (2, 1) | (2, 2):
                        pos[i] = move(pos[i], (1, 1))
                    case (-1, 2) | (-2, 1) | (-2, 2):
                        pos[i] = move(pos[i], (-1, 1))
                    case (1, -2) | (2, -1) | (2, -2):
                        pos[i] = move(pos[i], (1, -1))
                    case (-1, -2) | (-2, -1) | (-2, -2):
                        pos[i] = move(pos[i], (-1, -1))
                    case _:
                        pass  # adjacent
            visited.add(pos[-1])
    return visited


visited_p1 = track_tail(2)
print(f"Tail visited {len(visited_p1)} points when rope is 2 knots")

visited_p2 = track_tail(10)
print(f"Tail visited {len(visited_p2)} points when rope is 10 knots")
