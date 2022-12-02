import math

with open("input-01.txt", "r") as f:
    raw_input = f.readlines()

sum = 0
for r in raw_input:
    total_fuel = 0
    fuel = math.floor(float(r) / 3) - 2
    while fuel > 0:
        total_fuel += fuel
        fuel = math.floor(float(fuel) / 3) - 2

    sum += total_fuel

print(sum)
