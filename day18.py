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

    trees = {}
    blockers = {}

    labeled_nodes = start_positions + list(pos_to_key.keys())
    for source in labeled_nodes:
        # Assumes there's only one shortest path to every node.
        paths = nx.single_source_shortest_path(local, source)
        trees[source] = nx.Graph()
        blockers[source] = {}
        for target in labeled_nodes:
            if target not in paths:
                continue
            blockers[source][target] = set()
            last_node = None
            dist = 0
            for n in reversed(paths[target]):
                dist += 1
                if n in labeled_nodes:
                    if last_node is not None:
                        trees[source].add_edge(n, last_node, weight=dist)
                    last_node = n
                    dist = 0
                elif n in pos_to_door:
                    blockers[source][target].add(pos_to_door[n].lower())

    def weighted_neighbors(state):
        positions, inventory = state
        for i, pos in enumerate(positions):
            for new_pos, attributes in trees[pos][pos].items():
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

    def heuristic(state):
        positions, inventory = state
        cost = 0
        for pos in positions:
            tree = trees[pos].copy()
#            print('before', state, tree.edges, int(tree.size('weight')))
            to_remove = [key_to_pos[k] for k in inventory if key_to_pos[k] != pos]
            starts = set(start_positions)
            starts.discard(pos)
            to_remove += list(starts)
            while True:
                did_work = False
                for pos_rem in to_remove:
                    if tree.has_node(pos_rem) and tree.degree(pos_rem) == 1:
                        did_work = True
                        tree.remove_node(pos_rem)
                if not did_work:
                    break
#            print('after', state, tree.edges, int(tree.size('weight')))
            cost += int(tree.size('weight'))
        return cost

    def heuristic_check(state):
        cost = heuristic(state)
        for state2, _, length in dijkstra_edges(state, weighted_neighbors):
            if state2[1] == all_keys:
                real_cost = length
                break
        if cost > real_cost:
            raise Exception(f'inadmissible heuristic: {state2} {cost} > {real_cost}')
        return cost

    start_state = (tuple(start_positions), frozenset())
    for state, _, length in astar_edges(start_state, weighted_neighbors, heuristic):
        if state[1] == all_keys:
            return length

    raise

def change_to_part2(lines):
    rows = len(lines)
    cols = len(lines[0])
    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            if c == '@':
                lines[y][x] = '#'
                lines[y-1][x] = '#'
                lines[y+1][x] = '#'
                lines[y][x-1] = '#'
                lines[y][x+1] = '#'
                lines[y-1][x-1] = '@'
                lines[y-1][x+1] = '@'
                lines[y+1][x-1] = '@'
                lines[y+1][x+1] = '@'
                return

def compute_day18(input):
    part1 = None
    part1 = compute_shortest_steps(input, 1)
    print(f'part1: {part1}')
    lines = [[c for c in line.strip()] for line in input.strip().split('\n')]
    change_to_part2(lines)
    input_part2 = '\n'.join(''.join(line) for line in lines)
    part2 = compute_shortest_steps(input_part2, 4)
    print(f'part2: {part2}')

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        compute_day18(input)
