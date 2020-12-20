import numpy as np
import re

with open("23.txt", "r") as f:
	inputs = f.readlines()

# inputs = """pos=<10,12,12>, r=2
# pos=<12,14,12>, r=2
# pos=<16,12,12>, r=4
# pos=<14,14,14>, r=6
# pos=<50,50,50>, r=200
# pos=<10,10,10>, r=5""".split("\n")

def manhattan_distance(bot1, bot2):
	return abs(bot1[0] - bot2[0]) + \
		abs(bot1[1] - bot2[1]) + \
		abs(bot1[2] - bot2[2])

nanobots = []
for line in inputs:
	print(line)
	matches = re.search(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line)
	x = int(matches.group(1))
	y = int(matches.group(2))
	z = int(matches.group(3))
	r = int(matches.group(4))
	nanobots.append((x, y, z, r))

xvals = [0] + [n[0] for n in nanobots]
yvals = [0] + [n[1] for n in nanobots]
zvals = [0] + [n[2] for n in nanobots]

## Part 1:
# nanobots = sorted(nanobots, key=lambda x: x[3], reverse=True)
# biggest_nanobot = nanobots[0]
# count = 0
# for nanobot in nanobots:
# 	dist = manhattan_distance(biggest_nanobot, nanobot)
# 	if dist <= biggest_nanobot[3]:
# 		count += 1
# print(count)

step = 1
while step < max(xvals) - min(xvals):
    step *= 2

print(min(xvals), max(xvals), step)

while True:
	print(f"Step: {step}")
	best_count = 0
	best_answer = None
	best_spot = None
	for x in range(min(xvals), max(xvals) + 1, step):
		for y in range(min(yvals), max(yvals) + 1, step):
			for z in range(min(zvals), max(zvals) + 1, step):
				count = 0
				for nanobot in nanobots:
					manh_dist = abs(x - nanobot[0]) + abs(y - nanobot[1]) + abs(z - nanobot[2])
					if (manh_dist - nanobot[3]) // step <= 0:
						count += 1
				if count > best_count:
					best_count = count
					best_answer = abs(x) + abs(y) + abs(z)
					best_spot = (x, y, z)
				elif count == best_count and (best_answer is None or abs(x) + abs(y) + abs(z) < best_answer):
					best_count = count
					best_answer = abs(x) + abs(y) + abs(z)
					best_spot = (x, y, z)
	if step == 1:
		print(f"Part 2: best value {best_answer} at {best_spot}")
		break
	xvals = [best_spot[0] - step, best_spot[0] + step]
	yvals = [best_spot[1] - step, best_spot[1] + step]
	zvals = [best_spot[2] - step, best_spot[2] + step]
	step = step // 2


