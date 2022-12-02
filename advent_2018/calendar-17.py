import re

import numpy as np

with open("17.txt", "r") as f:
    inputs = f.readlines()

# inputs = """x=495, y=2..7
# y=7, x=495..501
# x=501, y=3..7
# x=498, y=2..4
# x=506, y=1..2
# x=498, y=10..13
# x=504, y=10..13
# y=13, x=498..504""".split("\n")


def print_terrain(terrain):
    temp_cav = np.copy(terrain)
    # for fighter in fighters:
    # 	temp_cav[fighter.y, fighter.x] = fighter.char
    for row in temp_cav:
        print(row.tostring().decode("utf8"))


def waterfall(terrain, free_water):
    # WATERFALL
    print(f"starting waterfall at {free_water[-1]}")
    if terrain[free_water[-1][1] + 1, free_water[-1][0]] != b".":
        print("nothing to waterfall")
        return
    if not np.any(terrain[free_water[-1][1] :, free_water[-1][0]] == b"#"):
        # Waterfall has no end!!!
        print("endless waterfall")
        terrain[free_water[-1][1] :, free_water[-1][0]] = "|"
        return
    bottom = free_water[-1][1] + np.argmax(
        terrain[free_water[-1][1] :, free_water[-1][0]] == b"#"
    )
    print("waterfall bottom at " + str(bottom))
    for i in range(free_water[-1][1], bottom):
        free_water.append((free_water[-1][0], i))
        terrain[i, free_water[-1][0]] = "|"
    return True


def spread(terrain, free_water):
    # SPREAD
    print(f"spread from {free_water[-1]}")
    if terrain[free_water[-1][1] + 1, free_water[-1][0]] in [b".", b"|"]:
        print("Skipping spread")
        # Already a waterfall
        return 0, 0
    left_index = free_water[-1][0] - 1
    while True:
        # Spread left
        if terrain[free_water[-1][1], left_index] == b"#":
            break
        if terrain[free_water[-1][1] + 1, left_index] == b"|":
            return 0, 0
        terrain[free_water[-1][1], left_index] = "|"
        left_index -= 1
        if terrain[free_water[-1][1] + 1, left_index] == b".":
            break
    right_index = free_water[-1][0] + 1
    while True:
        # Spread right
        if terrain[free_water[-1][1], right_index] == b"#":
            break
        if terrain[free_water[-1][1] + 1, right_index] == b"|":
            return 0, 0
        terrain[free_water[-1][1], right_index] = "|"
        right_index += 1
        if terrain[free_water[-1][1] + 1, right_index] == b".":
            break
    return left_index, right_index


def settle(terrain, free_water, left_index, right_index):
    # SETTLE
    is_open = False
    if terrain[free_water[-1][1], left_index] != b"#":
        terrain[free_water[-1][1], left_index] = "|"
        free_water.append((left_index, free_water[-1][1]))
        is_open = True
        print("left open")
    if terrain[free_water[-1][1], right_index] != b"#":
        terrain[free_water[-1][1], right_index] = "|"
        free_water.append((right_index, free_water[-1][1]))
        is_open = True
        print("right open")
    if is_open is False:
        terrain[free_water[-1][1], left_index + 1 : right_index] = "~"
        print("none open, deleting last")
        del free_water[-1]


coordinates = []
for line in inputs:
    x_match = re.search(r"x=([\d.]+)", line).group(1)
    y_match = re.search(r"y=([\d.]+)", line).group(1)
    if ".." in x_match:
        start = int(x_match.split("..")[0])
        end = int(x_match.split("..")[1])
        for i in range(start, end):
            coordinates.append((i, int(y_match)))
    elif ".." in y_match:
        start = int(y_match.split("..")[0])
        end = int(y_match.split("..")[1])
        for i in range(start, end + 1):
            coordinates.append((int(x_match), i))
    else:
        coordinates.append((int(x_match), int(y_match)))

x_min = min([c[0] for c in coordinates])
x_max = max([c[0] for c in coordinates])
y_min = min([c[1] for c in coordinates])
y_max = max([c[1] for c in coordinates])

terrain = np.chararray((y_max + 2, x_max + 2), itemsize=1)
terrain[:] = "."
for c in coordinates:
    terrain[c[1], c[0]] = "#"
terrain[0, 500] = "+"

print_terrain(terrain[:, x_min - 1 :])
print("=" * 50)
initial_terrain = terrain

water = np.chararray(terrain.shape)
free_water = [(500, 0)]


while True:

    if len(free_water) == 0:
        break

    waterfall(terrain, free_water)
    # print_terrain(terrain[:, x_min - 1:])
    # print("="*50)

    l_ind, r_ind = spread(terrain, free_water)
    # print_terrain(terrain[:, x_min - 1:])
    # print("="*50)

    if l_ind > 0 and r_ind > 0:
        settle(terrain, free_water, l_ind, r_ind)
    else:
        del free_water[-1]

    # print_terrain(terrain[:, x_min - 1:])
    # print("="*50)

terrain[500, 0] = b"*"
print_terrain(terrain[y_min : y_max + 1, x_min : x_max + 1])
print(
    np.sum(
        np.logical_or(terrain[y_min:y_max, :] == b"|", terrain[y_min:y_max, :] == b"~")
    )
)

print(np.sum(terrain[y_min:y_max, :] == b"~"))
