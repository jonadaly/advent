from pathlib import Path
import re
import numpy as np
import hashlib
import math
from typing import List, Tuple

def get_matches_for_hash(ignore_tile_id: int, hash_to_match: str) -> List[Tuple[str, str]]:
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

tiles = {}
for raw_tile in raw_tiles:
    tile_lines = raw_tile.split("\n")
    tile_id = int(tile_lines[0][5:-1])
    n_rows = len(tile_lines) - 1
    n_cols = len(tile_lines[1])
    tile_data = np.chararray((n_rows, n_cols), itemsize=1)
    for ind, tile_line in enumerate(tile_lines[1:]):
        tile_data[ind, :] = list(tile_line)
    tiles[tile_id] = tile_data

all_hashes = []
edge_hashes = {}
for tile_id, tile_data in tiles.items():
    hashes = {}
    hashes["N"] = hashlib.md5(bytes(tile_data[0,:])).hexdigest()
    hashes["S"] = hashlib.md5(bytes(tile_data[-1,:])).hexdigest()
    hashes["E"] = hashlib.md5(bytes(tile_data[:,-1])).hexdigest()
    hashes["W"] = hashlib.md5(bytes(tile_data[:,0])).hexdigest()
    hashes["Nf"] = hashlib.md5(bytes(np.flip(tile_data[0,:]))).hexdigest()
    hashes["Sf"] = hashlib.md5(bytes(np.flip(tile_data[-1,:]))).hexdigest()
    hashes["Ef"] = hashlib.md5(bytes(np.flip(tile_data[:,-1]))).hexdigest()
    hashes["Wf"] = hashlib.md5(bytes(np.flip(tile_data[:,0]))).hexdigest()
    edge_hashes[tile_id] = hashes
    all_hashes += hashes.values()

l = int(math.sqrt(len(tiles)))
corner_piece_ids = []
for tile_id, hashes in edge_hashes.items():
    unmatched_edges = 0
    for orientation in ["N", "S", "E", "W"]: # Assume corners won't match even if flipped
        num_instances = all_hashes.count(hashes[orientation])
        if num_instances == 1:
            unmatched_edges += 1
            # print(f"Tile ID {tile_id} orient {orientation} has no match")
    if unmatched_edges == 2:
        # Corner piece
        corner_piece_ids.append(tile_id)
result = np.product(corner_piece_ids)
print(f"Part 1: Product of corner piece IDs is {result}")

tile_positions = np.zeros([l, l], dtype=int)
# Start with any corner piece in the top left. Figure out the orientation.
tile_positions[0, 0] = corner_piece_ids[0]
unmatched_edges = []
for o in ["N", "S", "E", "W"]:
    hash_to_match = edge_hashes[tile_positions[0, 0]][o]
    candidates = get_matches_for_hash(ignore_tile_id=tile_positions[0, 0], hash_to_match=edge_hashes[tile_positions[0, 0]][o])
    if len(candidates) == 0:
        unmatched_edges.append(o)
# Corner pieces will have two unmatched edges. Use those to determine the orientation.
assert len(unmatched_edges) == 2


# Do the top row.
last_placed_tile_id = tile_positions[0, 0]
right_edge_hash = edge_hashes[last_placed_tile_id][get_opposite_edge(unmatched_edges[0])]
for i in range(1, l):
    candidates = get_matches_for_hash(ignore_tile_id=last_placed_tile_id ,hash_to_match=right_edge_hash)
    if len(candidates) == 0:
        print("NO EDGE MATCH")
        exit()
    if len(candidates) > 1:
        print("MULTIPLE EDGE MATCHES")
        exit()
    tile_positions[0, i] = candidates[0][0]
    last_placed_tile_id = tile_positions[0, i]
    right_edge_hash = edge_hashes[last_placed_tile_id][get_opposite_edge(candidates[0][1])]
    print(tile_positions)

# Do the left edge.
print("START LEFT")
last_placed_tile_id = tile_positions[0, 0]
bottom_edge_hash = edge_hashes[last_placed_tile_id][get_opposite_edge(unmatched_edges[1])]
for i in range(1, l):
    candidates = get_matches_for_hash(ignore_tile_id=last_placed_tile_id,hash_to_match=bottom_edge_hash)
    if len(candidates) == 0:
        print("NO EDGE MATCH")
        exit()
    if len(candidates) > 1:
        print("MULTIPLE EDGE MATCHES")
        exit()
    tile_positions[i, 0] = candidates[0][0]
    last_placed_tile_id = tile_positions[i, 0]
    bottom_edge_hash = edge_hashes[last_placed_tile_id][get_opposite_edge(candidates[0][1])]


    print(tile_positions)

