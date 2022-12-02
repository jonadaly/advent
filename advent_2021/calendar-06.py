from pathlib import Path

raw_fish = list(map(int, Path("06.txt").read_text().strip().split(",")))
fish = {i: sum(1 for fish in raw_fish if fish == i) for i in range(9)}
for i in range(256):
    fish = {
        8: fish[0],
        7: fish[8],
        6: fish[7] + fish[0],
        5: fish[6],
        4: fish[5],
        3: fish[4],
        2: fish[3],
        1: fish[2],
        0: fish[1],
    }
    if i in [79, 255]:
        print(f"After {i+1} days there are {sum(fish.values())} fish")
