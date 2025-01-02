from collections import defaultdict
from pathlib import Path


raw_pairs = Path("23.txt").read_text().strip().split("\n")

pairs = [tuple(r.split("-")) for r in raw_pairs]

connections = defaultdict(set)
for a, b in pairs:
    connections[a].add(b)
    connections[b].add(a)

all_connections = {p for p in pairs} | {(b, a) for a, b in pairs}

triples = set()
for c1, connected in connections.items():
    for c2 in connected:
        for c3 in connected.intersection(connections[c2]):
            triples.add(frozenset({c1, c2, c3}))


triples_with_t = {t for t in triples if any(c.startswith("t") for c in t)}
print(f"Part 1: {len(triples_with_t)} rings of 3 contain a name starting with t")

networks = [{c} for c in connections.keys()]
for network in networks:
    for computer in connections.keys():
        if all((computer, d) in all_connections for d in network):
            network.add(computer)
biggest_network = sorted(max(networks, key=len))
print(f"Part 2: the biggest network is {",".join(biggest_network)}")
