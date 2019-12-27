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

    key_distances = {}
    blockers = {}

    for source in start_positions + list(pos_to_key.keys()):
        # We assume there's only one shortest path to source (i.e.,
        # not another one that may avoid doors).
        paths = nx.single_source_shortest_path(local, source)
        key_distances[source] = {}
        blockers[source] = {}
        for target in pos_to_key.keys():
            if target not in paths:
                continue
            blockers[source][target] = set(pos_to_door[n].lower() for n in paths[target][1:] if n in pos_to_door)
            key_distances[source][target] = len(paths[target]) - 1

    def weighted_neighbors(state):
        positions, inventory, remainings = state
        for i, pos in enumerate(positions):
            remaining = remainings[i]
            for key in remaining:
                new_pos = key_to_pos[key]
                if inventory.issuperset(blockers[pos][new_pos]):
                    new_positions = tuple(positions[:i] + (new_pos,) + positions[i+1:])
                    delta = frozenset([key])
                    new_inventory = inventory | delta
                    new_remainings = tuple(remainings[:i] + (remaining - delta,) + remainings[i+1:])
                    new_state = (new_positions, new_inventory, new_remainings)
                    yield (new_state, key_distances[pos][new_pos])

    cache = {}
    def compute_min_distance_to_goal(state):
        key = state[0], state[1]
        if key in cache:
            return cache[key]

        min_distance = _compute_min_distance_to_goal(state)
        cache[key] = min_distance
        return min_distance

    all_keys = frozenset(key_to_pos.keys())
    def _compute_min_distance_to_goal(state):
        if state[1] == all_keys:
            return 0

        return min(cost + compute_min_distance_to_goal(next_state) for next_state, cost in weighted_neighbors(state))

    remainings = tuple(frozenset(pos_to_key[pos] for pos in blockers[start].keys()) for start in start_positions)
    start_state = (tuple(start_positions), frozenset(), remainings)
    return compute_min_distance_to_goal(start_state)

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
