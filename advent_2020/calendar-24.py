import math
import re
from pathlib import Path
from typing import Dict, Tuple

paths = Path("24.txt").read_text().strip().split("\n")
sin_60 = math.sin(math.pi / 3)
cos_60 = math.cos(math.pi / 3)

# Part 1
tiles: Dict[Tuple[float, float], bool] = {}
for path in paths:
    trimmed_path = (
        path.replace("ne", "").replace("sw", "").replace("se", "").replace("nw", "")
    )
    destination = {
        "e": len(re.findall(r"e", trimmed_path)),
        "ne": len(re.findall(r"ne", path)),
        "se": len(re.findall(r"se", path)),
        "w": len(re.findall(r"w", trimmed_path)),
        "nw": len(re.findall(r"nw", path)),
        "sw": len(re.findall(r"sw", path)),
    }
    x = round(
        destination["e"]
        + destination["ne"] * cos_60
        + destination["se"] * cos_60
        - destination["w"]
        - destination["nw"] * cos_60
        - destination["sw"] * cos_60,
        5,
    )
    y = round(
        destination["ne"] * sin_60
        + destination["nw"] * sin_60
        - destination["se"] * sin_60
        - destination["sw"] * sin_60,
        5,
    )
    tiles[(x, y)] = not tiles.get((x, y), False)
n_black = sum(tiles.values())
print(f"Part 1: {n_black} tiles are black")

# plt.scatter([t[0] for t in tiles.keys()], [t[1] for t in tiles.keys()], c=list(tiles.values()))
# plt.show()


def round_for_comparison(coords: Tuple[float, float]) -> Tuple[float, float]:
    return (round(coords[0], 2), round(coords[1], 2))


def advance_day(
    tiles: Dict[Tuple[float, float], bool]
) -> Dict[Tuple[float, float], bool]:
    # add surrounding white tiles.
    expanded_tiles = tiles.copy()
    for coords, flipped in tiles.items():
        if flipped is False:
            continue
        for surrounding in [
            (1, 0),
            (-1, 0),
            (cos_60, sin_60),
            (-cos_60, sin_60),
            (cos_60, -sin_60),
            (-cos_60, -sin_60),
        ]:
            new_coords = (
                round(coords[0] + surrounding[0], 5),
                round(coords[1] + surrounding[1], 5),
            )
            if round_for_comparison(new_coords) not in [
                round_for_comparison(t) for t in expanded_tiles.keys()
            ]:
                expanded_tiles[new_coords] = False

    # plt.scatter([t[0] for t in expanded_tiles.keys()], [t[1] for t in expanded_tiles.keys()], c=list(expanded_tiles.values()))
    # plt.show()

    new_tiles = expanded_tiles.copy()
    for coords, flipped in expanded_tiles.items():
        # print(f"Assessing tile {coords} ({flipped})")
        nearby_black = 0
        for cand, cand_flipped in expanded_tiles.items():
            # print(f"Trying nearby tile: {cand} ({cand_flipped})")
            if cand == coords:
                # print(f"same tile - skip it")
                continue
            if abs(coords[0] - cand[0]) > 1.0001 or abs(coords[1] - cand[1]) > 1.0001:
                # print(f"tile is not nearby")
                continue
            # print(f"tile is nearby")
            if cand_flipped:
                nearby_black += 1
        # print(f"tile {coords} has {nearby_black} nearby black tiles")
        if flipped and (nearby_black == 0 or nearby_black > 2):
            new_tiles[coords] = False
        if not flipped and nearby_black == 2:
            new_tiles[coords] = True
    # return new_tiles
    return {k: v for k, v in new_tiles.items() if v is True}


# Part 2:
for i in range(100):
    tiles = advance_day(tiles)
    n_black = sum(tiles.values())
    print(f"After {i+1} iteration, {n_black} tiles are black")
    # print(len(new_tiles))
    # import pprint
    # pprint.pprint(new_tiles)
    # plt.scatter([t[0] for t in new_tiles.keys()], [t[1] for t in new_tiles.keys()], c=list(new_tiles.values()))
    # plt.show()
