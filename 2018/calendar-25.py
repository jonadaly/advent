with open("25.txt", "r") as f:
	inputs = f.readlines()

# inputs = """1,-1,-1,-2
# -2,-2,0,1
# 0,2,1,3
# -2,3,-2,1
# 0,2,3,-2
# -1,-1,1,-2
# 0,-2,-1,0
# -2,2,3,-1
# 1,2,2,0
# -1,-2,0,-2""".split("\n")

stars = []
for line in inputs:
	s = line.split(",")
	stars.append((int(s[0]), int(s[1]), int(s[2]), int(s[3])))

constellations = [s for s in range(len(stars))]
print(constellations)
for i, star in enumerate(stars):
	for j, comp in enumerate(stars):
		if constellations[i] == constellations[j]:
			continue
		if abs(star[0] - comp[0]) + abs(star[1] - comp[1]) + abs(star[2] - comp[2]) + abs(star[3] - comp[3]) <= 3:
			# constellations[j] and constellations[i] are the same constellation
			constellations = [constellations[i] if c == constellations[j] else c for c in constellations]

print(constellations)
print(f"Part 1: there are {len(set(constellations))} constellations")