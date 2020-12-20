import numpy as np

with open("18.txt", "r") as f:
	raw_area = f.readlines()
	
# raw_area = """.#.#...|#.
# .....#|##|
# .|..|...#.
# ..|#.....#
# #.#|||#|#|
# ...#.||...
# .|....|...
# ||...#|.#|
# |.||||..|.
# ...#.|..|.""".split("\n")

def print_area(area):
	temp_cav = np.copy(area)
	for row in temp_cav:
		print(row.tostring().decode("utf8"))

def grow(state, index, combinations):
	pass

width = len(raw_area[0])
height = len(raw_area)
area = np.chararray((height, width), itemsize=1)
for ind, row in enumerate(raw_area):
	area[ind, :] = list(row)

print_area(area)
print("="*20)

n_woods = []
n_lumbers = []
for i in range(1000000000):
	new_area = np.copy(area)
	for i_row, row in enumerate(area):
		for i_col, element in enumerate(row):
			start_row = max(i_row - 1, 0)		
			end_row = min(i_row + 2, height)
			start_col = max(i_col - 1, 0)		
			end_col = min(i_col + 2, width)
			local = area[start_row:end_row, start_col:end_col]					
			if element == b".":
				if np.sum(local == b"|") >= 3:
					new_area[i_row, i_col] = "|"
				else:
					new_area[i_row, i_col] = "."
			elif element == b"|":
				if np.sum(local == b"#") >= 3:
					new_area[i_row, i_col] = "#"
				else:
					new_area[i_row, i_col] = "|"
			elif element == b"#":
				if np.sum(local == b"#") >= 2 and np.sum(local == b"|") >= 1:
					new_area[i_row, i_col] = "#"
				else:
					new_area[i_row, i_col] = "."
	area = new_area

	print(i)
	print_area(area)
	print("="*20)

	n_woods_this = np.sum(area == b"|")
	n_lumbers_this = np.sum(area == b"#")

	if n_woods_this in n_woods and n_lumbers_this in n_lumbers:
		if n_woods.index(n_woods_this) and n_lumbers.index(n_lumbers_this):
			pattern_start = n_lumbers.index(n_lumbers_this)
			pattern_end = i - 1
			print(f"Found pattern. {pattern_start}-{pattern_end}. Modulo {1 + pattern_end - pattern_start}")
			ind = pattern_start + ((1000000000 - pattern_start) % (1 + pattern_end - pattern_start))
			# for j in range(pattern_start, pattern_end + 100):
			# 	print(f"{j}: {pattern_start + ((j - pattern_start) % (1 + pattern_end - pattern_start))}")
			# print(ind_temp, ind_temp2, ind)
			print(f"Part 2: {n_woods[ind]} woods and {n_lumbers[ind]} lumberyards, score: {n_woods[ind]*n_lumbers[ind]}")
			break

	n_woods.append(n_woods_this)
	n_lumbers.append(n_lumbers_this)

	if i == 9:		
		print(f"Part 1: {n_woods_this} woods and {n_lumbers_this} lumberyards, score: {n_woods_this*n_lumbers_this}")

