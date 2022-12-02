from collections import defaultdict

with open("20.txt", "r") as f:
    guide = f.read()

# guide = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

branches = []
x, y = 10000, 10000  # Start somewhere in the middle
prev_x, prev_y = x, y
distances = defaultdict(int)
for char in guide[1:-1]:
    if char == "(":
        branches.append((x, y))
    elif char == ")":
        x, y = branches.pop()
    elif char == "|":
        x, y = branches[-1]
    else:
        if char == "N":
            y -= 1
        elif char == "S":
            y += 1
        elif char == "E":
            x += 1
        elif char == "W":
            x -= 1

        if distances[(x, y)] != 0:
            distances[(x, y)] = min(distances[(x, y)], distances[(prev_x, prev_y)] + 1)
        else:
            distances[(x, y)] = distances[(prev_x, prev_y)] + 1

    prev_x, prev_y = x, y

print(f"Part 1: Max distance is {max(distances.values())}")
print(
    f"Part 2: {len([x for x in distances.values() if x >= 1000])} rooms are over 1000 doors away"
)
