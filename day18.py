from graph import *
from util import *
import networkx as nx

def compute_shortest_steps(input):
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    start_pos = None
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
                start_pos = p
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

    if start_pos is None:
        raise

    def local_neighbors(n, walkables):
        return [m for m in dir_neighbors(n) if m in walkables]

    local = nx.Graph([(n, m) for n in walkables for m in local_neighbors(n, walkables)])

    blockers = {start_pos: frozenset()}
    for parent, child in nx.bfs_edges(local, start_pos):
        new_blockers = blockers[parent]
        if child in pos_to_door:
            new_blockers |= frozenset(pos_to_door[child].lower())
        blockers[child] = new_blockers

    G = nx.Graph()

    labeled_nodes = [ start_pos ] + list(pos_to_key.keys())
    for source in labeled_nodes:
        local_lengths = nx.shortest_path_length(local, source)
        for target in labeled_nodes:
            if target != source and target in local_lengths:
                G.add_edge(source, target, weight=local_lengths[target])

    def weighted_neighbors(state):
        pos, inventory = state
        for new_pos, attributes in G[pos].items():
            if new_pos == start_pos:
                continue
            if inventory.issuperset(blockers[new_pos]):
                new_inventory = inventory | frozenset([pos_to_key[new_pos]])
                new_state = (new_pos, new_inventory)
                yield (new_state, attributes['weight'])

    all_keys = frozenset(key_to_pos.keys())

    start_state = (start_pos, frozenset())
    for state, length in dijkstra_path_lengths(start_state, weighted_neighbors):
        if state[1] == all_keys:
            return length

    raise

def compute_day18(input):
    part1 = compute_shortest_steps(input)
    return part1, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
