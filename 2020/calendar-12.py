from pathlib import Path
import numpy as np
import math
from typing import Tuple

def translate(location: Tuple[int, int], translation: Tuple[int, int]) -> Tuple[int, int]:
    return (location[0] + translation[0], location[1] + translation[1])

def rotate(location: Tuple[int, int], angle_deg: int) -> Tuple[int, int]:
    rotated_x = (location[0]*np.cos(angle_deg*math.pi/180)) - (location[1]*np.sin(angle_deg*math.pi/180))
    rotated_y = (location[1]*np.cos(angle_deg*math.pi/180)) + (location[0]*np.sin(angle_deg*math.pi/180))
    return (round(rotated_x), round(rotated_y))

instructions = Path("12.txt").read_text().strip().split("\n")

# Part 1
heading = 90
ship_position = (0,0)
for instruction in instructions:
    direc = instruction[0]
    value = int(instruction[1:])
    if direc == "F":
        if heading == 0:
            ship_position = translate(ship_position, (0, value))
        elif heading == 90:
            ship_position = translate(ship_position, (value, 0))
        elif heading == 180:
            ship_position = translate(ship_position, (0, -value))
        elif heading == 270:
            ship_position = translate(ship_position, (-value, 0))
        else:
            raise ValueError(f"Unexpected heading {heading}")
    elif direc == "L":
        heading  = (heading - value) % 360
    elif direc == "R":
        heading  = (heading + value) % 360
    elif direc == "N":
        ship_position = translate(ship_position, (0, value))
    elif direc == "S":
        ship_position = translate(ship_position, (0, -value))
    elif direc == "E":
        ship_position = translate(ship_position, (value, 0))
    elif direc == "W":
        ship_position = translate(ship_position, (-value, 0))
    else:
        raise ValueError(f"Unexpected value {value}")
print(f"Part 1: Manhattan distance: {abs(ship_position[0]) + abs(ship_position[1])}")

# Part 2
waypoint = (10, 1)
ship_position = (0, 0)
for instruction in instructions:
    direc = instruction[0]
    value = int(instruction[1:])
    if direc == "F":
        ship_position = translate(ship_position, (value*waypoint[0], value*waypoint[1]))
    elif direc == "L":
        waypoint = rotate(waypoint, value)
    elif direc == "R":
        waypoint = rotate(waypoint, -value)
    elif direc == "N":
        waypoint = translate(waypoint, (0, value))
    elif direc == "S":
        waypoint = translate(waypoint, (0, -value))
    elif direc == "E":
        waypoint = translate(waypoint, (value, 0))
    elif direc == "W":
        waypoint = translate(waypoint, (-value, 0))
    else:
        raise ValueError(f"Unexpected value {value}")
print(f"Part 2: Manhattan distance: {abs(ship_position[0]) + abs(ship_position[1])}")