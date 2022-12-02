import numpy as np
from scipy import ndimage

SERIAL = 6548

grid = np.zeros((300, 300))

x_coords = np.array([range(1, 301)])

rack_id = np.tile(x_coords.T, (1, 300)) + 10
grid = np.multiply(rack_id, np.tile(x_coords, (300, 1))) + SERIAL
grid = np.multiply(grid, rack_id)
test = np.char.mod("%d", grid / 100 % 10)
test2 = test.astype(float) - 5

biggest_val = -99999
biggest_coord = None
biggest_size = None
for size in range(1, 301):
    result = ndimage.uniform_filter(test2, size=size, mode="constant", cval=-99999999)
    maxval = np.amax(result) * size * size
    print(f"size: {size}, maxval: {maxval}")
    if maxval > biggest_val:
        maxloc = np.argmax(result)
        maxxoord = np.unravel_index(maxloc, result.shape)
        biggest_val = maxval
        biggest_coord = maxxoord
        biggest_size = size
        print(biggest_val, biggest_coord, biggest_size)

print(biggest_coord, biggest_size)
