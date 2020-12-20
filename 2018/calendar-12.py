initial_state = "####..##.##..##..#..###..#....#.######..###########.#...#.##..####.###.#.###.###..#.####..#.#..##..#"

rules = """.#.## => .
...## => #
..#.. => .
#.#.. => .
...#. => .
.#... => #
..... => .
#.... => .
#...# => #
###.# => .
..### => #
###.. => .
##.## => .
##.#. => #
..#.# => #
.###. => .
.#.#. => .
.##.. => #
.#### => .
##... => .
##### => .
..##. => .
#.##. => .
.#..# => #
##..# => .
#.#.# => #
#.### => .
....# => .
#..#. => #
#..## => .
####. => #
.##.# => #"""

# initial_state = "#..#.#..##......###...###"

# rules = """...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #"""

N_GEN = 50000000000

combinations = [r[:5] for r in rules.split("\n") if r.endswith("#")]

def grow(state, index, combinations):
	index -= 5
	old_state = list("....." + state + ".....")
	new_state = old_state[:]
	for i in range(2, len(old_state) - 2):
		sequence = "".join(old_state[i-2:i+3])		
		new_state[i] = "#" if sequence in combinations else "."
	new_state_string = "".join(new_state)
	trim_l = new_state_string.find("#")
	trim_r = new_state_string.rfind("#")
	return new_state_string[trim_l:trim_r+1], index + trim_l

index = 0
state = initial_state
print(state)
for i in range(N_GEN):
	new_state, new_index = grow(state, index, combinations)
	print(f"{new_index} {new_state}")
	if (state == new_state):
		# Reached equlibrium
		difference_per_gen = new_index - index
		index += (N_GEN - i) * difference_per_gen
		break
	state = new_state
	index = new_index	

print(sum([k + index for k, v in enumerate(state) if v == "#"]))