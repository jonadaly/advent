from anytree import Node, RenderTree

with open("8.txt", 'r') as f:
	inputs = f.read()

# inputs = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

node_id = 0

def add_node(raw_data, parent=None) -> Node:
	global node_id
	n_children = raw_data[0]
	n_metadata = raw_data[1]
	node = Node(node_id, parent=parent, metadata=None, size=-1)
	node_id += 1
	child_raw_data = raw_data[2:]
	for n in range(n_children):
		child_node = add_node(child_raw_data, node)
		child_raw_data = child_raw_data[child_node.size:]
	node.metadata = child_raw_data[:n_metadata]
	node.size = len(raw_data) - len(child_raw_data) + n_metadata
	return node

raw_data = [int(i) for i in inputs.split()]

root = add_node(raw_data)

total = 0
for pre, fill, node in RenderTree(root):
	print(f"{pre}{node.name}: {node.metadata}")
	total += sum(node.metadata)

print(f"Part 1: sum is {total}")

def get_value(node):
	if len(node.children) == 0:
		return sum(node.metadata)
	# Node has children.
	value = 0
	for m in node.metadata:
		if m > 0 and m <= len(node.children):
			value += get_value(node.children[m-1])
	return value

root_value = get_value(root)
print(f"Part 2: root value is {root_value}")
