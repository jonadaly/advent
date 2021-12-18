import ast
import itertools
import math
from pathlib import Path
from typing import Optional


def build_tree(
    value: list,
    tree: Optional[dict] = None,
    node_id: Optional[int] = 1,
):
    """
    Use this pattern for ids:
    -----1-----
    ---2---3---
    --4-5-6-7--
    etc
    """
    if tree is None:
        tree = {}
    if isinstance(value, int):
        tree[node_id] = value
    else:
        build_tree(value[0], node_id=node_id * 2, tree=tree)
        build_tree(value[1], node_id=(node_id * 2) + 1, tree=tree)
    return tree


def explode_or_split(tree_original: dict) -> dict:
    """
    Here we need to make use of the node IDs to do some tricks. To find the node on the left/right (required for
    exploding), we order the keys by their binary representation (alphabetically) to get tree traversal order.
    e.g. node 5 (0b101) is to the right of node 2 (0b10), but to the left of node 3 (0b11).
    """
    tree = tree_original.copy()  # Don't mutate the original, silly!

    # Sort binary representation of keys alphabetically. This gives node traversal order (depth first, left to right).
    keys = sorted(tree.keys(), key=lambda n: "{0:b}".format(n))

    # First, try to explode.
    for i_order, node_id in enumerate(keys):
        if node_id < 32:
            continue
        left_value = tree[node_id]
        right_value = tree[node_id + 1]
        parent_id = node_id // 2
        if i_order > 0:
            # There is a node to the left.
            tree[keys[i_order - 1]] += left_value
        if i_order < len(keys) - 2:
            # There is a node to the right (ignoring the other half of the pair).
            tree[keys[i_order + 2]] += right_value
        tree[parent_id] = 0
        del tree[node_id]
        del tree[node_id + 1]
        return tree

    # Next, try to split.
    for i_order, node_id in enumerate(keys):
        if tree[node_id] > 9:
            tree[node_id * 2] = tree[node_id] // 2
            tree[node_id * 2 + 1] = math.ceil(tree[node_id] / 2)
            del tree[node_id]
            return tree

    return tree


def reduce(tree: dict) -> dict:
    while True:
        new_t = explode_or_split(tree)
        if tree == new_t:
            return tree
        tree = new_t


def add(tree1: dict, tree2: dict) -> dict:
    """
    To add two numbers you need them to form each side of a new tree. There's probably some clever maths you
    can do to figure out what the new index of each value is, but I couldn't figure it out so I hacked it. Make
    it binary (e.g. 'Ob1011'), then replace the first digit with '10' for the first number (to make it the left side
    of the tree) and '11' for the second number (to make it the right side of the tree).
    """
    t1_updated = {int("0b10" + bin(k)[3:], 2): v for k, v in tree1.items()}
    t2_updated = {int("0b11" + bin(k)[3:], 2): v for k, v in tree2.items()}
    return reduce({**t1_updated, **t2_updated})


def sum_all(all_numbers: list) -> dict:
    running_number = all_numbers[0]
    for next_number in all_numbers[1:]:
        running_number = add(running_number, next_number)
    return running_number


def magnitude(number: dict) -> int:
    """
    For each node, if it's on the left side the last digit of the ID (in binary) is 0 and if it's on the
    right it's 1. So for each node you can work out what to multiply the value by based on the binary ID
    (ignoring the first digit because you always finish on node 1). E.g. if node 11 (0b1011) contains a value,
    the value should be multiplied by 2, then 2, then 3.
    """
    total = 0
    for k, v in number.items():
        bin_representation = bin(k)
        for digit in bin_representation[3:]:
            v *= 3 if digit == "0" else 2
        total += v
    return total


# Testing
# fmt: off
assert explode_or_split(build_tree([[[[[9,8],1],2],3],4])) == build_tree([[[[0,9],2],3],4])
assert explode_or_split(build_tree([7,[6,[5,[4,[3,2]]]]])) == build_tree([7,[6,[5,[7,0]]]])
assert explode_or_split(build_tree([[6,[5,[4,[3,2]]]],1])) == build_tree([[6,[5,[7,0]]],3])
assert explode_or_split(build_tree([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])) == build_tree([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
assert explode_or_split(build_tree([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])) == build_tree([[3,[2,[8,0]]],[9,[5,[7,0]]]])
assert add(build_tree([[[[4,3],4],4],[7,[[8,4],9]]]), build_tree([1,1])) == build_tree([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
assert magnitude(build_tree([[1,2],[[3,4],5]])) == 143
assert magnitude(build_tree([[[[0,7],4],[[7,8],[6,0]]],[8,1]])) == 1384
assert magnitude(build_tree([[[[1,1],[2,2]],[3,3]],[4,4]])) == 445
assert magnitude(build_tree([[[[3,0],[5,3]],[4,4]],[5,5]])) == 791
assert magnitude(build_tree([[[[5,0],[7,4]],[5,5]],[6,6]])) == 1137
assert magnitude(build_tree([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])) == 3488
test_numbers_raw = Path("18-example.txt").read_text().strip().split("\n")
test_numbers = [build_tree(ast.literal_eval(r)) for r in test_numbers_raw]
assert magnitude(sum_all(test_numbers)) == 4140
# fmt: on

# The real thing
actual_numbers_raw = Path("18.txt").read_text().strip().split("\n")
actual_numbers = [build_tree(ast.literal_eval(r)) for r in actual_numbers_raw]
sum_magnitude = magnitude(sum_all(actual_numbers))
max_magnitude = max(
    magnitude(sum_all(pair))
    for pair in itertools.product(actual_numbers, actual_numbers)
    if pair[0] == pair[1]
)
print(f"Part 1: magnitude of sum of all numbers is {sum_magnitude}")
print(f"Part 2: max magnitude of any pair sum is {max_magnitude}")
