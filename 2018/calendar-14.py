from collections import deque
import pprint


N_RECIPES = "323081"

recipes = [3, 7]
elf1_ind = 0
elf2_ind = 1
current_ind = 0

print(recipes, elf1_ind, elf2_ind)

for i in range(100000000):

	combined = recipes[elf1_ind] + recipes[elf2_ind]
	for digit in str(combined):
		recipes.append(int(digit))

	elf1_ind = (elf1_ind + 1 + recipes[elf1_ind]) % len(recipes)
	elf2_ind = (elf2_ind + 1 + recipes[elf2_ind]) % len(recipes)

	# if len(recipes) >= N_RECIPES + 10:
	# 	break

	
str_version = "".join(map(str, recipes))
# print(str_version)
if str_version.find(N_RECIPES) > -1:
	print(str_version.find(N_RECIPES))
else :
	print("NOPE")


# print(recipes)
# print("".join(map(str, recipes[N_RECIPES:N_RECIPES+10])))
