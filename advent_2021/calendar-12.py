from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set

connections_raw = Path("12.txt").read_text().strip().split("\n")

graph: Dict[str, List[str]] = defaultdict(list)
for connection_raw in connections_raw:
    node1, node2 = connection_raw.split("-")
    graph[node1].append(node2)
    graph[node2].append(node1)


def traverse_nodes(
    paths: List[List[str]],
    current_node: str,
    current_path: List[str],
    allowed_multiple_node: Optional[str] = None,
) -> None:
    current_path.append(current_node)
    for vertex in graph[current_node]:
        if vertex not in current_path or not vertex.islower():
            traverse_nodes(paths, vertex, current_path.copy(), allowed_multiple_node)
        elif vertex == allowed_multiple_node:
            traverse_nodes(paths, vertex, current_path.copy(), None)
    paths.append(current_path)


all_paths_part1 = []
traverse_nodes(all_paths_part1, "start", [], None)
possible_paths_part1: Set[str] = {
    ",".join(v) for v in all_paths_part1 if v[-1] == "end"
}
print(f"Part 1: {len(possible_paths_part1)} possible paths")

all_paths_part2 = []
for node in set(graph.keys()) - {"start", "end"}:
    traverse_nodes(all_paths_part2, "start", [], node)
possible_paths_part2: Set[str] = {
    ",".join(v) for v in all_paths_part2 if v[-1] == "end"
}
print(f"Part 2: {len(possible_paths_part2)} possible paths")
