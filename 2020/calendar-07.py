from pathlib import Path
import re
from py2neo import Graph
import json
import numpy as np

graph = Graph(host="localhost")
graph.delete_all()
raw_rules = Path("07-example.txt").read_text().strip()
rules = re.findall(r"^(.+) bags contain (.+)\.$", raw_rules, re.M)

for outer_colour, _ in rules:
    graph.run("CREATE (b:Bag {colour: {colour}}) RETURN b", {"colour": outer_colour})

for outer_colour, inner_bags in rules:
    if inner_bags == "no other bags":
        continue
    inner_bag_colours = inner_bags.split(", ")
    for ibc in inner_bag_colours:
        match = re.match(r"(\d+) (.+) bag(s?)", ibc)
        count = match.groups()[0]
        inner_colour = match.groups()[1]
        query = """
        MATCH (p:Bag),(c:Bag)
        WHERE p.colour = {p_colour} AND c.colour = {c_colour}
        CREATE (p)-[r:CONTAINS {count: {count}}]->(c)
        RETURN type(r)
        """
        graph.run(
            query, {"p_colour": outer_colour, "c_colour": inner_colour, "count": count}
        )

# Part 1
bags = graph.run(
    "MATCH (b:Bag)-[:CONTAINS*]->(t:Bag) WHERE t.colour = 'shiny gold' RETURN SIZE(COLLECT(DISTINCT b.colour)) AS result"
).data()
print(f"Part 1: {bags[0]['result']} bags can contain shiny gold bag")

# Part 2
paths = graph.run(
    "MATCH path = (b:Bag)-[r:CONTAINS*]->(c:Bag) WHERE b.colour = 'shiny gold' RETURN RELATIONSHIPS(path) as rel"
).data()
total = 0
for path in paths:
    n_bags = [int(r["count"]) for r in path["rel"]]
    total += np.product(n_bags)
print(f"Part 2: {total} total bags")
