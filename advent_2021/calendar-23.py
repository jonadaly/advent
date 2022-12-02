from typing import List, Tuple

import networkx as nx
from networkx import shortest_path, shortest_path_length

BANNED = {2, 4, 6, 8}
HALL_POS_LOOKUP = {"A": 2, "B": 4, "C": 6, "D": 8}
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def find_last_dot(arg):
    """Helper to guard for the ValueError."""
    try:
        return "".join(arg).rindex(".")
    except ValueError:
        return 0


def room_available(_state: list, room: str):
    """
    Checks whether a room is available to be moved into. If the room is available, returns a tuple of
    True and the index of the next available space. If the room is unavailable, returns a tuple of
    False and the index of the outermost occupied space.
    """
    if room == "A":
        if all(s in [".", "A"] for s in _state[11:15]):
            return True, 11 + find_last_dot(_state[11:15])
        else:
            return False, next(
                i for i, s in enumerate(_state) if 11 <= i < 15 and s != "."
            )
    if room == "B":
        if all(s in [".", "B"] for s in _state[15:19]):
            return True, 15 + find_last_dot(_state[15:19])
        else:
            return False, next(
                i for i, s in enumerate(_state) if 15 <= i < 19 and s != "."
            )
    if room == "C":
        if all(s in [".", "C"] for s in _state[19:23]):
            return True, 19 + find_last_dot(_state[19:23])
        else:
            return False, next(
                i for i, s in enumerate(_state) if 19 <= i < 23 and s != "."
            )
    if room == "D":
        if all(s in [".", "D"] for s in _state[23:27]):
            return True, 23 + find_last_dot(_state[23:27])
        else:
            return False, next(
                i for i, s in enumerate(_state) if 23 <= i < 27 and s != "."
            )
    raise ValueError


def is_path(_state: list, hall_pos: int, room: str):
    """Calculates whether there is a path between the specified hall position and room."""
    if hall_pos >= HALL_POS_LOOKUP[room]:
        return all(s == "." for s in _state[HALL_POS_LOOKUP[room] : hall_pos])
    else:
        return all(s == "." for s in _state[hall_pos + 1 : HALL_POS_LOOKUP[room]])


def length_path(start: int, end: int) -> int:
    """Calculates the length of a path between two spaces in the burrow."""
    start_hall = start
    end_hall = end
    start_room_extra = 0
    end_room_extra = 0
    if start >= 11:
        start_hall = 2 + (2 * ((start - 11) // 4))
        start_room_extra = ((start - 11) % 4) + 1
    if end >= 11:
        end_hall = 2 + (2 * ((end - 11) // 4))
        end_room_extra = ((end - 11) % 4) + 1
    return abs(start_hall - end_hall) + start_room_extra + end_room_extra


assert length_path(1, 18) == 7
assert length_path(18, 1) == 7
assert length_path(5, 19) == 2
assert length_path(19, 5) == 2
assert length_path(10, 11) == 9
assert length_path(11, 10) == 9


def print_state(_state: list):
    print("#############")
    print(f"#{''.join(_state[:11])}#")
    print(f"###{_state[11]}#{_state[15]}#{_state[19]}#{_state[23]}###")
    print(f"  #{_state[12]}#{_state[16]}#{_state[20]}#{_state[24]}#  ")
    print(f"  #{_state[13]}#{_state[17]}#{_state[21]}#{_state[25]}#  ")
    print(f"  #{_state[14]}#{_state[18]}#{_state[22]}#{_state[26]}#  ")
    print("  #########  ")


def find_possible_moves(_state: list) -> List[Tuple[List, int]]:
    """
    Finds all possible moves from the specifed state and returns a list of tuples, where the first element is
    the new state after the move, and the second element is the cost of getting to the new state.
    """
    possible_moves: List[Tuple[list, int]] = []

    # See if any of the ones in the hall can move.
    for i_start, s in enumerate(_state[:11]):
        _new_state = _state.copy()
        for room in ("A", "B", "C", "D"):
            if s == room and is_path(_state, i_start, room):
                available, i_end = room_available(_state, room)
                if available:
                    _new_state[i_start] = "."
                    _new_state[i_end] = room
                    possible_moves.append(
                        (_new_state, COST[room] * length_path(i_start, i_end))
                    )

    # See if any of the ones in the rooms can move.
    for room in ("A", "B", "C", "D"):
        start_room_available, i_to_move = room_available(_state, room)
        # print(f"Room {room} is available: {start_room_available}")
        if start_room_available:
            # Room is already available, no need to move anything out.
            continue
        value_to_move = _state[i_to_move]
        available, i_end = room_available(_state, value_to_move)
        if available and is_path(_state, HALL_POS_LOOKUP[room], value_to_move):
            # Can move straight into destination room.
            _new_state = _state.copy()
            _new_state[i_to_move] = "."
            _new_state[i_end] = value_to_move
            possible_moves.append(
                (_new_state, COST[value_to_move] * length_path(i_to_move, i_end))
            )
        else:
            # Try each hallway position.
            for i_space, space in enumerate(_state[:11]):
                if (
                    i_space not in BANNED
                    and space == "."
                    and is_path(_state, i_space, room)
                ):
                    _new_state = _state.copy()
                    _new_state[i_to_move] = "."
                    _new_state[i_space] = value_to_move
                    possible_moves.append(
                        (
                            _new_state,
                            COST[value_to_move] * length_path(i_to_move, i_space),
                        )
                    )
    return possible_moves


# start_state = "...........BDDACCBDBBACDACA"  # test input
start_state = "...........DDDBACBABBADCACC"  # real input
end_state = "...........AAAABBBBCCCCDDDD"

state_graph = nx.Graph()
state_graph.add_node(start_state)


def build_graph(_graph, _state, depth):
    if _state == list(end_state):
        # print("FINISHED!")
        return
    possible_moves = find_possible_moves(_state)
    if len(possible_moves) == 0:
        # print("DEAD END")
        return
    print(f"{'-'*depth}> (depth {depth}) found {len(possible_moves)} possible moves")
    for new_state, cost in possible_moves:
        if not state_graph.has_node("".join(new_state)):
            state_graph.add_node("".join(new_state))
            state_graph.add_edge("".join(_state), "".join(new_state), cost=cost)
            build_graph(_graph, new_state, depth + 1)  # recurse
        else:
            state_graph.add_edge("".join(_state), "".join(new_state), cost=cost)


build_graph(state_graph, list(start_state), depth=1)
path = shortest_path(
    state_graph, source=start_state, target=end_state, weight="cost", method="dijkstra"
)
path_length = shortest_path_length(
    state_graph, source=start_state, target=end_state, weight="cost", method="dijkstra"
)

for p in path:
    print_state(list(p))

# Solved part 1 by hand.
print("Part 1: Least energy required is 15516")

print(f"Part 2: Least energy required is {path_length}")
