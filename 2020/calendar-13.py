from pathlib import Path
import sys

instructions = Path("13.txt").read_text().strip().split("\n")
timestamp = int(instructions[0])

def get_first_bus_after(timestamp, bus):
    minutes_before = timestamp % bus
    bus_time = timestamp - minutes_before
    if minutes_before > 0:
        bus_time = timestamp - minutes_before + bus
    return bus_time

# Part 1
earliest_bus = None
result = None
for bus in ([int(b) for b in instructions[1].split(",") if b != "x"]):
    bus_time = get_first_bus_after(timestamp, bus)
    if earliest_bus is None or bus_time < earliest_bus:
        earliest_bus = bus_time
        result = bus * (earliest_bus - timestamp)
print(f"Part 1: result is {result}")

# Part 2
buses = ([b for b in instructions[1].split(",")])
timestamp = 0
step_size = 1
for i, b in enumerate(buses):
    if b == "x":
        continue
    while True:
        if (timestamp + i) % int(b) == 0:
            step_size *= int(b)
            break
        timestamp += step_size
print(f"Part 2: timestamp is {timestamp}")