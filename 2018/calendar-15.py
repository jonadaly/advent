import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

# raw_cavern = """#########
# #G..G..G#
# #.......#
# #.......#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #########""".split("\n")

# raw_cavern = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######""".split("\n")

# raw_cavern = """#######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######""".split("\n")

# raw_cavern = """#######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# #######""".split("\n")

# raw_cavern = """#######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######""".split("\n")

# raw_cavern = """#######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######""".split("\n")

# raw_cavern = """#########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########""".split("\n")

raw_cavern = """################################
#################..#############
#################.##############
#################.####..########
############G..G...###..########
##########...G...........#######
##########.#.......#.G##########
########...#.....#...G..########
#######G.###............G#######
###########..G..#.......########
####..#####............#########
###.G.###.......G.....G.########
###..#####....#####.......######
####..#####..#######........E..#
#.##..####..#########.........E#
#....###.GG.#########........###
##....#.G...#########.......####
#....G...G..#########......#####
#..........G#########.....######
#.....G......#######......######
#........##...#####.......######
#G###...##............#....#####
#..#######................E#####
#.########...............#######
#..#######..............########
#####..#....E...##.......#######
#####.G#.......#.E..#EE.########
#####...E....#....#..###########
#######.......E....E.###########
#######.###....###.....#########
#######.####.######.....########
################################""".split("\n")

# raw_cavern = """################################
# #####################...########
# ###################....G########
# ###################....#########
# #######.##########......########
# #######G#########........#######
# #######G#######.G.........######
# #######.######..G.........######
# #######.......##.G...G.G..######
# ########..##..#....G......G#####
# ############...#.....G.....#####
# #...#######..........G.#...#####
# #...#######...#####G......######
# ##...######..#######G.....#.##.#
# ###.G.#####.#########G.........#
# ###G..#####.#########.......#.E#
# ###..######.#########..........#
# ###.......#.#########.....E..E.#
# #####G...#..#########.......#..#
# ####.G.#.#...#######.....G.....#
# ########......#####...........##
# ###########..................###
# ##########.................#####
# ##########.................#####
# ############..E.........E.....##
# ############.........E........##
# ###############.#............E##
# ##################...E..E..##.##
# ####################.#E..####.##
# ################.....######...##
# #################.#..###########
# ################################""".split("\n")

FINDER = AStarFinder(diagonal_movement=DiagonalMovement.never)

class Fighter:

	def __init__(self, x, y, char):
		self.x = x
		self.y = y
		self.char = char
		self.hp = 200

	def __repr__(self):
		return f"Fighter '{self.char}' at ({self.x}, {self.y}), {self.hp} HP"

	def get_open_adjacent_spaces(self, fighters):
		global cavern
		temp_cav = np.copy(cavern)
		for fighter in fighters:
			if fighter.hp > 0:
				temp_cav[fighter.y, fighter.x] = fighter.char
		open_spaces = []
		if temp_cav[self.y - 1, self.x] == b".":
			open_spaces.append((self.x, self.y - 1))
		if temp_cav[self.y + 1, self.x] == b".":
			open_spaces.append((self.x, self.y + 1))
		if temp_cav[self.y, self.x - 1] == b".":
			open_spaces.append((self.x - 1, self.y))
		if temp_cav[self.y, self.x + 1] == b".":
			open_spaces.append((self.x + 1, self.y))
		return open_spaces

	def is_surrounded(self, fighters):
		global cavern
		temp_cav = np.copy(cavern)
		for fighter in fighters:
			if fighter.hp > 0:
				temp_cav[fighter.y, fighter.x] = fighter.char
		return (temp_cav[self.y - 1, self.x] != b"." and 
			temp_cav[self.y + 1, self.x] != b"." and 
			temp_cav[self.y, self.x + 1] != b"." and 
			temp_cav[self.y, self.x - 1] != b".")

	def has_targets(self, fighters):
		for fighter in fighters:
			if fighter.char != self.char and fighter.hp > 0:
				return True
		return False

	@classmethod
	def find_path(cls, point_from, point_to, fighters) -> list:
		global cavern
		temp_cav = cavern == b"."
		for fighter in fighters:
			if fighter.hp > 0:
				temp_cav[fighter.y, fighter.x] = False
		# Except the two ends
		temp_cav[point_from[1], point_from[0]] = True
		temp_cav[point_to[1], point_to[0]] = True

		optimal_path = cls._find_path(temp_cav, point_from, point_to)

		if not optimal_path:
			return None

		# What if there's another path?
		paths = [optimal_path]
		while True:
			temp_cav[paths[-1][1][1], paths[-1][1][0]] = False
			latest_path = cls._find_path(temp_cav, point_from, point_to)
			if not latest_path or len(latest_path) > len(optimal_path):
				break
			paths.append(latest_path)
		
		return [p for p in sorted(paths, key=lambda a: a[1][1]*999999 + a[1][0])][0]

	def get_weakest_adjacent_enemy(self, fighters):
		adjacent = []
		for fighter in fighters:
			if fighter.char == self.char or fighter.hp <= 0:
				continue
			if fighter.x == self.x:
				if fighter.y == self.y + 1 or fighter.y == self.y - 1:
					adjacent.append(fighter)
			elif fighter.y == self.y:
				if fighter.x == self.x + 1 or fighter.x == self.x - 1:
					adjacent.append(fighter)
		if len(adjacent) == 0:
			return None
		if len(adjacent) == 1:
			return adjacent[0]
		min_hp = min([a.hp for a in adjacent])
		lowest = [a for a in adjacent if a.hp == min_hp]
		reading_order = sorted(lowest, key=lambda m: m.y*999999 + m.x)
		return reading_order[0]

	@classmethod
	def _find_path(cls, temp_cav, point_from, point_to):
		matrix = temp_cav.astype(int)
		# print(matrix)
		grid = Grid(matrix=matrix)
		start = grid.node(point_from[0], point_from[1])
		end = grid.node(point_to[0], point_to[1])
		path, runs = FINDER.find_path(start, end, grid)
		# print('operations:', runs, 'path length:', len(path))
		# print(grid.grid_str(path=path, start=start, end=end))
		return path

def print_cavern(cavern, fighters):
	temp_cav = np.copy(cavern)
	for fighter in fighters:
		if fighter.hp > 0:
			temp_cav[fighter.y, fighter.x] = fighter.char
	for row in temp_cav:
		print(row.tostring().decode("utf8"))
	for f in fighters:
		print(f)


def simulate(elf_power = 3):

	any_dead_elf = False

	global cavern
	cavern = np.chararray((len(raw_cavern), len(raw_cavern[0])), itemsize=1)
	for ind, row in enumerate(raw_cavern):
		cavern[ind, :] = list(row)

	fighters = []
	for y, row in enumerate(cavern):
		for x, spot in enumerate(row):
			if spot in [b"G", b"E"]:
				fighters.append(Fighter(x, y, spot))

	cavern[np.isin(cavern, [b"G", b"E"])] = b"."

	print_cavern(cavern, fighters)

	targets_exist = True
	count = 0
	while targets_exist is True and any_dead_elf is False:
		for fighter in sorted(fighters, key=lambda f: f.y*9999999 + f.x):

			if fighter.hp <= 0:
				# Fighter is dead.
				continue

			if fighter.has_targets(fighters) is False:
				targets_exist = False
				print(f"{fighter}: ABORT - no targets left")
				continue

			target = fighter.get_weakest_adjacent_enemy(fighters)
			if target is not None:
				print(f"{fighter}: Skipping movement, adjacent enemy {target}")
				pass
			else:

				open_spaces = []
				for cand_target in fighters:
					if cand_target.char == fighter.char or cand_target.hp <= 0:
						# Same team or dead
						continue
					open_spaces += cand_target.get_open_adjacent_spaces(fighters)
				
				if len(open_spaces) == 0:
					# No open spaces
					continue

				path = None
				path_length = 999999
				# print(f"{fighter} has open spaces {open_spaces}")
				for open_space in sorted(open_spaces, key=lambda s: s[1]*99999 + s[0]):
					cand_path = Fighter.find_path((fighter.x, fighter.y), open_space, fighters)
					if cand_path is not None and len(cand_path) < path_length:
						path_length = len(cand_path)
						path = cand_path

				if path is None:
					# No accessible spaces
					continue

				# Move towards target.
				# print(f"{fighter} has path {path}")
				fighter.x = path[1][0]
				fighter.y = path[1][1]

			target = fighter.get_weakest_adjacent_enemy(fighters)
			if target is None:
				print(f"{fighter}: No target in range, not attacking")
				continue
				
			print(f"{fighter}: Attacking weakest adjacent enemy {target}")
			if fighter.char == b"E":
				target.hp -= elf_power
			else:
				target.hp -= 3
			if target.hp <= 0:
				print(f"{fighter}: Fighter is dead: {target}")
				if target.char == b"E":
					any_dead_elf = True
				target.char = b"."

		count += 1
		print(f"end of round {count}")
		print_cavern(cavern, fighters)
		print("------")

	total_hp = sum([f.hp for f in fighters if f.hp > 0])
	# print(f"Part 1: {count - 1} full rounds, {total_hp} total HP remaining. Score {total_hp*(count - 1)}")
	return any_dead_elf, total_hp, count - 1

elf_power = 11
cavern = None
while True:
	any_dead_elf, total_hp, rounds = simulate(elf_power)
	print(f"\n\n----------->power {elf_power} done, any_dead_elf: {any_dead_elf}, total_hp: {total_hp}, rounds: {rounds}")
	if any_dead_elf is False:
		print(f"Part 2: {rounds} full rounds, {total_hp} total HP remaining. Score {total_hp*rounds}")
		break
	elf_power += 1
#167280

#191812

#184556

# 196789

