import hashlib
import math
from pathlib import Path
from typing import Dict, List, Tuple

# import re
import numpy as np
import regex as re


class Tile:
    def __init__(self, id: int, elements: np.ndarray):
        self.id = id
        self.elements = elements
        self._calculate_hashes()

    def rotate(self):
        self.elements = np.rot90(self.elements)
        self._calculate_hashes()

    def flipud(self):
        self.elements = np.flipud(self.elements)
        self._calculate_hashes()

    def fliplr(self):
        self.elements = np.fliplr(self.elements)
        self._calculate_hashes()

    def _calculate_hashes(self):
        hashes = {}
        hashes["N"] = hashlib.md5(bytes(self.elements[0, :])).hexdigest()
        hashes["S"] = hashlib.md5(bytes(self.elements[-1, :])).hexdigest()
        hashes["E"] = hashlib.md5(bytes(self.elements[:, -1])).hexdigest()
        hashes["W"] = hashlib.md5(bytes(self.elements[:, 0])).hexdigest()
        hashes["Nf"] = hashlib.md5(bytes(np.flip(self.elements[0, :]))).hexdigest()
        hashes["Sf"] = hashlib.md5(bytes(np.flip(self.elements[-1, :]))).hexdigest()
        hashes["Ef"] = hashlib.md5(bytes(np.flip(self.elements[:, -1]))).hexdigest()
        hashes["Wf"] = hashlib.md5(bytes(np.flip(self.elements[:, 0]))).hexdigest()
        self.hashes = hashes

    def __repr__(self):
        result = ""
        for row in self.elements:
            result += row.tostring().decode("utf8")
            result += "\n"
        return result


def match_tile(
    original_tile: Tile, original_edge: str, all_tiles: Dict[int, Tile]
) -> Tile:
    """
    Returns a matching tile, oriented correctly.
    """
    matching_tile = None
    hash_to_match = original_tile.hashes[original_edge]
    opposite_edge = get_opposite_edge(original_edge)
    for tile in all_tiles.values():
        if tile.id == original_tile.id:
            continue
        if hash_to_match in tile.hashes.values():
            matching_tile = tile
    while True:
        if matching_tile.hashes[opposite_edge] == hash_to_match:
            break
        matching_tile.flipud()
        if matching_tile.hashes[opposite_edge] == hash_to_match:
            break
        matching_tile.fliplr()
        if matching_tile.hashes[opposite_edge] == hash_to_match:
            break
        matching_tile.rotate()
    return matching_tile


def get_matches_for_hash(
    ignore_tile_id: int, hash_to_match: str
) -> List[Tuple[str, str]]:
    # Find a piece matching this edge.
    candidates = []
    for tile_id, hashes in edge_hashes.items():
        if tile_id == ignore_tile_id:
            # Same tile.
            continue
        for k, v in hashes.items():
            if v == hash_to_match:
                # print(f"Found match {k} of tile {v}")c
                candidates.append((tile_id, k))
    return candidates


def get_opposite_edge(edge: str) -> str:
    if edge == "N":
        return "S"
    if edge == "S":
        return "N"
    if edge == "E":
        return "W"
    if edge == "W":
        return "E"
    if edge == "Nf":
        return "Sf"
    if edge == "Sf":
        return "Nf"
    if edge == "Ef":
        return "Wf"
    if edge == "Wf":
        return "Ef"


raw_tiles = Path("20.txt").read_text().strip().split("\n\n")

tile_map = {}
tiles: Dict[int, Tile] = {}
for raw_tile in raw_tiles:
    tile_lines = raw_tile.split("\n")
    tile_id = int(tile_lines[0][5:-1])
    n_rows = len(tile_lines) - 1
    n_cols = len(tile_lines[1])
    tile_data = np.chararray((n_rows, n_cols), itemsize=1)
    for ind, tile_line in enumerate(tile_lines[1:]):
        tile_data[ind, :] = list(tile_line)
    tile_map[tile_id] = tile_data
    tiles[tile_id] = Tile(tile_id, tile_data)

all_hashes = []
edge_hashes = {}
for tile_id, tile_data in tile_map.items():
    hashes = {}
    hashes["N"] = hashlib.md5(bytes(tile_data[0, :])).hexdigest()
    hashes["S"] = hashlib.md5(bytes(tile_data[-1, :])).hexdigest()
    hashes["E"] = hashlib.md5(bytes(tile_data[:, -1])).hexdigest()
    hashes["W"] = hashlib.md5(bytes(tile_data[:, 0])).hexdigest()
    hashes["Nf"] = hashlib.md5(bytes(np.flip(tile_data[0, :]))).hexdigest()
    hashes["Sf"] = hashlib.md5(bytes(np.flip(tile_data[-1, :]))).hexdigest()
    hashes["Ef"] = hashlib.md5(bytes(np.flip(tile_data[:, -1]))).hexdigest()
    hashes["Wf"] = hashlib.md5(bytes(np.flip(tile_data[:, 0]))).hexdigest()
    edge_hashes[tile_id] = hashes
    all_hashes += hashes.values()

_l = int(math.sqrt(len(tile_map)))
corner_piece_ids = []
for tile_id, hashes in edge_hashes.items():
    unmatched_edges = 0
    for orientation in [
        "N",
        "S",
        "E",
        "W",
    ]:  # Assume corners won't match even if flipped
        num_instances = all_hashes.count(hashes[orientation])
        if num_instances == 1:
            unmatched_edges += 1
            # print(f"Tile ID {tile_id} orient {orientation} has no match")
    if unmatched_edges == 2:
        # Corner piece
        corner_piece_ids.append(tile_id)
# print(f"Corner piece IDs: {corner_piece_ids}")
result = np.product(corner_piece_ids)
print(f"Part 1: Product of corner piece IDs is {result}")

tile_positions = np.zeros([_l, _l], dtype=int)

# TOP LEFT CORNER
top_left_corner_tile = tiles[corner_piece_ids[0]]
while True:
    top_count = all_hashes.count(top_left_corner_tile.hashes["N"])
    left_count = all_hashes.count(top_left_corner_tile.hashes["W"])
    if top_count == 1 and left_count == 1:
        break
    top_left_corner_tile.rotate()
tile_positions[0, 0] = top_left_corner_tile.id

# TOP EDGE
last_placed_tile = top_left_corner_tile
for i in range(1, _l):
    matching_tile = match_tile(last_placed_tile, "E", tiles)
    assert last_placed_tile.hashes["E"] == matching_tile.hashes["W"]
    tile_positions[0, i] = matching_tile.id
    last_placed_tile = matching_tile

# COLUMNS
for i_row in range(1, _l):
    for i_col in range(_l):
        last_placed_tile = tiles[tile_positions[i_row - 1, i_col]]
        matching_tile = match_tile(last_placed_tile, "S", tiles)
        assert last_placed_tile.hashes["S"] == matching_tile.hashes["N"]
        tile_positions[i_row, i_col] = matching_tile.id

image_rows = []
for i_row in range(_l):
    row_of_tiles = [
        tiles[tile_positions[i_row, i]].elements[1:9, 1:9] for i in range(_l)
    ]
    image_rows.append(np.concatenate(row_of_tiles, 1))
final_image = np.concatenate(image_rows, 0)

image_length = len(final_image[0, :])
line_gap = image_length - 20
monster_regex = f"#.{{{line_gap + 1}}}#.{{4}}##.{{4}}##.{{4}}###.{{{line_gap + 1}}}#.{{2}}#.{{2}}#.{{2}}#.{{2}}#.{{2}}#"
matches = None
for i in range(8):
    final_image = np.rot90(final_image)
    one_liner = "".join([row.tobytes().decode("utf8") for row in final_image])
    matches = re.findall(monster_regex, one_liner, overlapped=True)
    if len(matches) > 0:
        break
    if i == 4:
        final_image = np.fliplr(final_image)
N_HASHES_IN_MONSTER = 15
total_hashes = np.sum(final_image == b"#")
print(f"Part 2: roughness is {total_hashes - len(matches)*N_HASHES_IN_MONSTER}")
