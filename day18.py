from graph import *
from util import *
import networkx as nx

def compute_shortest_steps(input, start_count):
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    start_positions = []
    pos_to_key = {}
    key_to_pos = {}
    pos_to_door = {}
    door_to_pos = {}
    walkables = set()

    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            if c == '#':
                continue
            p = (x, y)
            if c == '@':
                start_positions.append(p)
            elif c == '.':
                pass
            elif 'a' <= c <= 'z':
                pos_to_key[p] = c
                key_to_pos[c] = p
            elif 'A' <= c <= 'Z':
                pos_to_door[p] = c
                door_to_pos[c] = p
            else:
                raise

            walkables.add(p)

    if len(start_positions) != start_count:
        raise

    local = nx.Graph([(n, m) for n in walkables for m in dir_neighbors(n) if m in walkables])

    G = nx.Graph()
    blockers = {}

    labeled_nodes = start_positions + list(pos_to_key.keys())
    for source in labeled_nodes:
        # Assumes there's only one shortest path to every node.
        paths = nx.single_source_shortest_path(local, source)
        blockers[source] = {}
        for target in labeled_nodes:
            blockers[source][target] = set()
            path = paths[target]
            last_node = None
            dist = 0
            for n in reversed(path):
                dist += 1
                if n in labeled_nodes:
                    if last_node is not None:
                        G.add_edge(n, last_node, weight=dist)
                    last_node = n
                    dist = 0
                elif n in pos_to_door:
                    blockers[source][target].add(pos_to_door[n].lower())

    def weighted_neighbors(state):
        positions, inventory = state
        for i, pos in enumerate(positions):
            for new_pos, attributes in G[pos].items():
                _positions = list(positions)
                _positions[i] = new_pos
                new_positions = tuple(_positions)
                if new_pos in start_positions:
                    new_state = (new_positions, inventory)
                    yield (new_state, attributes['weight'])
                elif inventory.issuperset(blockers[pos][new_pos]):
                    new_inventory = inventory | frozenset([pos_to_key[new_pos]])
                    new_state = (new_positions, new_inventory)
                    yield (new_state, attributes['weight'])

    all_keys = frozenset(key_to_pos.keys())

    start_state = (tuple(start_positions), frozenset())
    for state, length in dijkstra_path_lengths(start_state, weighted_neighbors):
        if state[1] == all_keys:
            return length

    raise

def compute_day18(input):
    part1 = compute_shortest_steps(input, 1)
    return part1, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
