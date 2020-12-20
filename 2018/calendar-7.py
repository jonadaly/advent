inputs = """Step I must be finished before step Q can begin.
Step B must be finished before step O can begin.
Step J must be finished before step M can begin.
Step W must be finished before step Y can begin.
Step U must be finished before step X can begin.
Step T must be finished before step Q can begin.
Step G must be finished before step M can begin.
Step K must be finished before step C can begin.
Step F must be finished before step Z can begin.
Step D must be finished before step A can begin.
Step N must be finished before step Y can begin.
Step Y must be finished before step Q can begin.
Step Q must be finished before step Z can begin.
Step V must be finished before step E can begin.
Step A must be finished before step X can begin.
Step E must be finished before step C can begin.
Step O must be finished before step R can begin.
Step P must be finished before step L can begin.
Step H must be finished before step R can begin.
Step M must be finished before step R can begin.
Step C must be finished before step Z can begin.
Step R must be finished before step L can begin.
Step L must be finished before step S can begin.
Step S must be finished before step X can begin.
Step Z must be finished before step X can begin.
Step T must be finished before step O can begin.
Step D must be finished before step Z can begin.
Step P must be finished before step R can begin.
Step M must be finished before step Z can begin.
Step L must be finished before step Z can begin.
Step W must be finished before step N can begin.
Step Q must be finished before step R can begin.
Step P must be finished before step C can begin.
Step U must be finished before step O can begin.
Step F must be finished before step O can begin.
Step K must be finished before step X can begin.
Step G must be finished before step K can begin.
Step M must be finished before step C can begin.
Step Y must be finished before step Z can begin.
Step A must be finished before step O can begin.
Step D must be finished before step P can begin.
Step K must be finished before step S can begin.
Step I must be finished before step E can begin.
Step G must be finished before step F can begin.
Step S must be finished before step Z can begin.
Step N must be finished before step V can begin.
Step F must be finished before step D can begin.
Step A must be finished before step Z can begin.
Step F must be finished before step X can begin.
Step T must be finished before step Y can begin.
Step W must be finished before step H can begin.
Step D must be finished before step H can begin.
Step W must be finished before step G can begin.
Step J must be finished before step X can begin.
Step T must be finished before step X can begin.
Step U must be finished before step R can begin.
Step O must be finished before step P can begin.
Step L must be finished before step X can begin.
Step I must be finished before step B can begin.
Step M must be finished before step L can begin.
Step C must be finished before step R can begin.
Step R must be finished before step X can begin.
Step F must be finished before step N can begin.
Step V must be finished before step H can begin.
Step K must be finished before step A can begin.
Step W must be finished before step O can begin.
Step U must be finished before step Q can begin.
Step O must be finished before step C can begin.
Step K must be finished before step V can begin.
Step R must be finished before step S can begin.
Step E must be finished before step S can begin.
Step J must be finished before step A can begin.
Step E must be finished before step X can begin.
Step K must be finished before step Y can begin.
Step Y must be finished before step X can begin.
Step P must be finished before step Z can begin.
Step W must be finished before step X can begin.
Step Y must be finished before step A can begin.
Step V must be finished before step X can begin.
Step O must be finished before step M can begin.
Step I must be finished before step J can begin.
Step W must be finished before step L can begin.
Step I must be finished before step G can begin.
Step D must be finished before step O can begin.
Step D must be finished before step N can begin.
Step M must be finished before step X can begin.
Step I must be finished before step R can begin.
Step Y must be finished before step M can begin.
Step F must be finished before step M can begin.
Step U must be finished before step M can begin.
Step Y must be finished before step H can begin.
Step K must be finished before step D can begin.
Step N must be finished before step O can begin.
Step H must be finished before step S can begin.
Step G must be finished before step L can begin.
Step T must be finished before step D can begin.
Step J must be finished before step N can begin.
Step K must be finished before step M can begin.
Step K must be finished before step P can begin.
Step E must be finished before step R can begin.
Step N must be finished before step H can begin."""

# inputs = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""

import requests
import json
import pprint

steps = inputs.split("\n")

nodes = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# nodes = "ABCDEF"

query = "CREATE "
for node in nodes:
	query += f"(s{node}:Step{{label: '{node}', assigned: false}}), "

for step in steps:
	prereq = step[5]
	req = step[36]
	query += f"(s{prereq})-[d{prereq}{req}:ENABLES]->(s{req}), "


response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
	"statements": [
		{
			"statement": "MATCH (n) DETACH DELETE n"
		},
		{
			"statement": query[:-2]
		}
	]
})

trail = []
response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
	"statements": [
		{
			"statement": "MATCH (s:Step) WHERE NOT (s)<-[:ENABLES]-() return s.label"
		}
	]
})
# pprint.pprint(response.json())
available_nodes = [s["row"][0] for s in response.json()["results"][0]["data"]]
trail.append(sorted(available_nodes)[0])

while True:
	response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
		"statements": [
			{
				"statement": f"MATCH (s:Step) WHERE s.label = '{trail[-1]}' DETACH DELETE s"
			},
			{
				"statement": "MATCH (s:Step) WHERE NOT (s)<-[:ENABLES]-() return s.label"
			}
		]
	})
	# pprint.pprint(response.json())
	available_nodes = [s["row"][0] for s in response.json()["results"][1]["data"]]
	if len(available_nodes) == 0:
		break
	trail.append(sorted(available_nodes)[0])

print(f"Part 1: {''.join(trail)}")

# PART 2!!!

BUFFER = 60
WORKERS = 5

response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
	"statements": [
		{
			"statement": "MATCH (n) DETACH DELETE n"
		},
		{
			"statement": query[:-2]
		}
	]
})

trail = []
elapsed = 0
work_to_do = {nodes[i]: i+1+BUFFER for i in range(len(nodes))}
assignment = {i: None for i in range(WORKERS)}
tasks_remaining = True
# pprint.pprint(work_to_do)
while tasks_remaining:

	response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
		"statements": [
			{
				"statement": "MATCH (s:Step) WHERE NOT (s)<-[:ENABLES]-() return s.label"
			}
		]
	})
	all_remaining_nodes = sorted([s["row"][0] for s in response.json()["results"][0]["data"]])
	if len(all_remaining_nodes) == 0:
		tasks_remaining = False
		break

	for w in range(WORKERS):
		if (assignment[w] is None or work_to_do[assignment[w]] == 0):			

			# Start new assignment
			response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
				"statements": [
					{
						"statement": f"MATCH (s:Step) WHERE s.label = '{assignment[w]}' DETACH DELETE s"
					}
				]
			})						
			response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
				"statements": [
					{
						"statement": "MATCH (s:Step) WHERE NOT (s)<-[:ENABLES]-() AND s.assigned = false return s.label"
					}
				]
			})
			available_nodes = sorted([s["row"][0] for s in response.json()["results"][0]["data"]])
			if len(available_nodes) == 0:
				assignment[w] = None
				continue
			assignment[w] = available_nodes.pop(0)
			trail.append(assignment[w])
			response = requests.post("http://localhost:7474/db/data/transaction/commit", json={
				"statements": [
					{
						"statement": f"MATCH (s:Step) WHERE s.label = '{assignment[w]}' SET s.assigned = true RETURN s"
					}
				]
			})	

		work_to_do[assignment[w]] -= 1
		
	elapsed += 1
	print(elapsed)
	# pprint.pprint(assignment)
	# pprint.pprint(work_to_do)

print(trail)
print(f"Part 2: elapsed time {elapsed-1} seconds")