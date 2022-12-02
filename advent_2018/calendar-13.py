import numpy as np


class Cart:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.crashed = False
        self.intersection_count = 0

    def __repr__(self):
        return f"Cart: ({self.x}, {self.y}), orientation {self.char}"


def print_track(current_track, current_carts):
    temp_track = np.copy(current_track)
    for cart in current_carts:
        temp_track[cart.y, cart.x] = cart.char
    for row in temp_track:
        print(row.tostring().decode("utf8"))


with open("13-rob.txt", "r") as f:
    raw_track = f.read().split("\n")

track = np.chararray((len(raw_track), len(raw_track[0])), itemsize=1)

carts = []
for ind, row in enumerate(raw_track):
    # print(ind, row)
    track[ind, :] = list(row)

for y, row in enumerate(track):
    for x, seg in enumerate(row):
        if seg in [b"v", b">", b"<", b"^"]:
            carts.append(Cart(x, y, seg))

track[np.isin(track, [b"<", b">"])] = b"-"
track[np.isin(track, [b"^", b"v"])] = b"|"

# print_track(track, carts)
for i in range(100000):
    for c in sorted(carts, key=lambda c: c.y * 1000 + c.x):
        if c.crashed is True:
            continue
        if c.char == b">":
            c.x += 1
        elif c.char == b"<":
            c.x -= 1
        elif c.char == b"^":
            c.y -= 1
        elif c.char == b"v":
            c.y += 1
        else:
            raise ValueError(f"unexpected char {c.char}")

        # Check crashed

        for d in carts:
            if (
                c.x == d.x
                and c.y == d.y
                and c.char != d.char
                and c.crashed is False
                and d.crashed is False
            ):
                print(f"CRASH on iteration {i} at ({c.x}, {c.y})")
                c.crashed = True
                c.char = b"x"
                d.crashed = True
                d.char = b"x"
                crashed = True

        new_track_segment = track[c.y, c.x]
        if new_track_segment == b"/":
            if c.char == b">":
                c.char = b"^"
            elif c.char == b"^":
                c.char = b">"
            elif c.char == b"<":
                c.char = b"v"
            elif c.char == b"v":
                c.char = b"<"
        if new_track_segment == b"\\":
            if c.char == b"<":
                c.char = b"^"
            elif c.char == b"^":
                c.char = b"<"
            elif c.char == b">":
                c.char = b"v"
            elif c.char == b"v":
                c.char = b">"
        if new_track_segment == b"+":
            if c.intersection_count % 3 == 0:
                if c.char == b">":
                    c.char = b"^"
                elif c.char == b"^":
                    c.char = b"<"
                elif c.char == b"<":
                    c.char = b"v"
                elif c.char == b"v":
                    c.char = b">"
            if c.intersection_count % 3 == 2:
                if c.char == b">":
                    c.char = b"v"
                elif c.char == b"v":
                    c.char = b"<"
                elif c.char == b"<":
                    c.char = b"^"
                elif c.char == b"^":
                    c.char = b">"
            c.intersection_count += 1

    uncrashed_carts = [x for x in carts if x.crashed is False]
    if len(uncrashed_carts) == 1:
        # print_track(track, carts)
        print(
            f"Only 1 uncrashed cart left at ({uncrashed_carts[0].x},{uncrashed_carts[0].y})"
        )
        break
    elif len(uncrashed_carts) == 0:
        print("No uncrashed carts!!!")
        exit()
    # print_track(track, carts)

# print_track(track, carts)
# for cart in carts:
# 	print(cart)
