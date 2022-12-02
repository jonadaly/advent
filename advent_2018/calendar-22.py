from enum import Enum

import networkx as nx
import numpy as np

DEPTH = 3339
TARGET = (10, 715)
# DEPTH = 510
# TARGET = (10,10)

EXTRA = 100


class Gear(Enum):
    TORCH = 0
    CLIMBING = 1
    NEITHER = 2


def get_possible_items(char):
    if char == b".":
        return [Gear.TORCH, Gear.CLIMBING]
    if char == b"=":
        return [Gear.CLIMBING, Gear.NEITHER]
    if char == b"|":
        return [Gear.NEITHER, Gear.TORCH]
    return [Gear.TORCH, Gear.CLIMBING, Gear.NEITHER]


geologic_index = np.zeros((TARGET[1] + EXTRA, TARGET[0] + EXTRA))
geologic_index[:, 0] = np.arange(TARGET[1] + EXTRA) * 48271
geologic_index[0, :] = np.arange(TARGET[0] + EXTRA) * 16807

erosion_level = (geologic_index + DEPTH) % 20183


for i_row, row in enumerate(geologic_index):
    if i_row == 0:
        continue
    for i_col, col in enumerate(row):
        if i_col == 0:
            continue
        geologic_index[i_row, i_col] = (
            erosion_level[i_row - 1, i_col] * erosion_level[i_row, i_col - 1]
        )
        erosion_level[i_row, i_col] = (geologic_index[i_row, i_col] + DEPTH) % 20183

terrain = np.chararray(geologic_index.shape)
terrain[erosion_level % 3 == 0] = "."
terrain[erosion_level % 3 == 1] = "="
terrain[erosion_level % 3 == 2] = "|"
terrain[0, 0] = "M"
terrain[TARGET[1], TARGET[0]] = "T"
print(geologic_index)
print(erosion_level)
print("\n".join(["".join(row.decode("utf8")) for row in terrain]))

risk_level = np.sum(terrain[: TARGET[1] + 1, : TARGET[0] + 1] == b"=") + (
    2 * np.sum(terrain[: TARGET[1] + 1, : TARGET[0] + 1] == b"|")
)
print(f"Part 1: risk level is {risk_level}")

# Part 2: build graph out of x and y coordinates, using tool changes as another dimension
graph = nx.Graph()
for index, value in np.ndenumerate(terrain):
    y, x = index
    possible_items = get_possible_items(value)
    # Add edge between weapons
    graph.add_edge((x, y, possible_items[0]), (x, y, possible_items[1]), weight=7)
    if x > 0:
        next_items = get_possible_items(terrain[y, x - 1])
        for item in set(possible_items).intersection(set(next_items)):
            graph.add_edge((x, y, item), (x - 1, y, item), weight=1)
    if x < TARGET[0] + EXTRA - 1:
        next_items = get_possible_items(terrain[y, x + 1])
        for item in set(possible_items).intersection(set(next_items)):
            graph.add_edge((x, y, item), (x + 1, y, item), weight=1)
    if y > 0:
        next_items = get_possible_items(terrain[y - 1, x])
        for item in set(possible_items).intersection(set(next_items)):
            graph.add_edge((x, y, item), (x, y - 1, item), weight=1)
    if y < TARGET[1] + EXTRA - 1:
        next_items = get_possible_items(terrain[y + 1, x])
        for item in set(possible_items).intersection(set(next_items)):
            graph.add_edge((x, y, item), (x, y + 1, item), weight=1)

test = nx.dijkstra_path_length(
    graph, (0, 0, Gear.TORCH), (TARGET[0], TARGET[1], Gear.TORCH)
)
print(test)
