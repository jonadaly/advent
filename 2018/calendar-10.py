with open("10.txt", 'r') as f:
	inputs = f.read().strip()

# inputs = """position=< 9,  1> velocity=< 0,  2>
# position=< 7,  0> velocity=<-1,  0>
# position=< 3, -2> velocity=<-1,  1>
# position=< 6, 10> velocity=<-2, -1>
# position=< 2, -4> velocity=< 2,  2>
# position=<-6, 10> velocity=< 2, -2>
# position=< 1,  8> velocity=< 1, -1>
# position=< 1,  7> velocity=< 1,  0>
# position=<-3, 11> velocity=< 1, -2>
# position=< 7,  6> velocity=<-1, -1>
# position=<-2,  3> velocity=< 1,  0>
# position=<-4,  3> velocity=< 2,  0>
# position=<10, -3> velocity=<-1,  1>
# position=< 5, 11> velocity=< 1, -2>
# position=< 4,  7> velocity=< 0, -1>
# position=< 8, -2> velocity=< 0,  1>
# position=<15,  0> velocity=<-2,  0>
# position=< 1,  6> velocity=< 1,  0>
# position=< 8,  9> velocity=< 0, -1>
# position=< 3,  3> velocity=<-1,  1>
# position=< 0,  5> velocity=< 0, -1>
# position=<-2,  2> velocity=< 2,  0>
# position=< 5, -2> velocity=< 1,  2>
# position=< 1,  4> velocity=< 2,  1>
# position=<-2,  7> velocity=< 2, -2>
# position=< 3,  6> velocity=<-1, -1>
# position=< 5,  0> velocity=< 1,  0>
# position=<-6,  0> velocity=< 2,  0>
# position=< 5,  9> velocity=< 1, -2>
# position=<14,  7> velocity=<-2,  0>
# position=<-3,  6> velocity=< 2, -1>"""

import re
import numpy as np
from matplotlib import pyplot as plt

pattern = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)>\s*velocity=<\s*(-?\d+),\s*(-?\d+)>')
x_init = np.array([])
y_init = np.array([])
x_dot = np.array([])
y_dot = np.array([])
for star in inputs.split("\n"):
	match = pattern.search(star)
	if match is None:
		print("HERE", star)
	x_init = np.append(x_init, float(match.group(1)))
	y_init = np.append(y_init, float(match.group(2)))
	x_dot = np.append(x_dot, float(match.group(3)))
	y_dot = np.append(y_dot, float(match.group(4)))

x_std = np.array([])
y_std = np.array([])
x_latest = []
y_latest = []
for i in range(100000):
	print(i)
	x_new = x_init + (x_dot * i)
	y_new = y_init + (y_dot * i)
	x_new_std = np.std(x_new)
	y_new_std = np.std(y_new)
	if i > 1 and x_new_std > x_std[-1]:
		break	
	x_std = np.append(x_std, x_new_std)
	y_std = np.append(y_std, y_new_std)
	x_latest = x_new
	y_latest = y_new

plt.scatter(-x_latest, y_latest)
plt.show()
