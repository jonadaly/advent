import numpy as np


trail = np.genfromtxt("10.txt", delimiter=1, dtype=int)
is_trailhead = np.where(trail == 0)
trailheads = is_trailhead[0] + 1j * is_trailhead[1]


def dfs(trail, current, peaks):
    current_height = trail[int(current.real), int(current.imag)]
    for step in [-1, 1, -1j, 1j]:
        new = current + step
        if (
            new.real < 0
            or new.imag < 0
            or new.real >= trail.shape[0]
            or new.imag >= trail.shape[1]
        ):
            # Off the edge of the map
            continue
        new_height = trail[int(new.real), int(new.imag)]
        if new_height != current_height + 1:
            # Dead end
            continue
        if new_height == 9:
            # Found a peak
            peaks.append(new)
            continue
        # Recurse
        dfs(trail, new, peaks)


scores: list[int] = []
ratings: list[int] = []
for trailhead in trailheads:
    peaks: list[complex] = []
    dfs(trail, trailhead, peaks)
    scores.append(len(set(peaks)))
    ratings.append(len(peaks))
print(f"Part 1: score is {sum(scores)}")
print(f"Part 2: rating is {sum(ratings)}")
