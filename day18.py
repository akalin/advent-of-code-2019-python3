from graph import *
from itertools import chain
from util import *
import timeit

def parse_map(input, start_count):
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    start_positions = []
    key_to_pos = {}
    pos_to_key = {}
    pos_to_door = {}
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
                key_to_pos[c] = p
                pos_to_key[p] = c
            elif 'A' <= c <= 'Z':
                pos_to_door[p] = c
            else:
                raise

            walkables.add(p)

    if len(start_positions) != start_count:
        raise

    def neighbors(n):
        return [m for m in dir_neighbors(n) if m in walkables]

    key_distances = {}
    key_objects = {}

    # For each possible position, BFS over the walkable graph to
    # compute distances to each key and intermediate doors/keys.
    for source, source_pos in chain(enumerate(start_positions), key_to_pos.items()):
        # We assume there's only one shortest path to each target
        # (i.e., not another one that may avoid doors).
        dists = {source_pos: 0}
        objs = {source_pos: ''}
        for parent, child in bfs_edges(source_pos, neighbors):
            dists[child] = dists[parent] + 1
            objs[child] = objs[parent]
            # Treat doors and keys equally, as we actually don't want
            # to pick up extra keys on the way to another one.
            if child in pos_to_door:
                objs[child] += pos_to_door[child].lower()
            elif child in pos_to_key:
                objs[child] += pos_to_key[child]

        key_distances[source] = {target: dists[target_pos] for target, target_pos in key_to_pos.items() if target_pos in dists}
        # The last entry in objs[target_pos] is target itself.
        key_objects[source] = {target: frozenset(objs[target_pos][:-1]) for target, target_pos in key_to_pos.items() if target_pos in objs}

    key_to_index = {}
    for i in range(start_count):
        for key in key_distances[i].keys():
            key_to_index[key] = i

    # A state is a tuple of positions and an inventory of keys. A
    # position is either a number (representing one of the starting
    # positions) or a key.

    # The successors of a given state are the states where we acquire
    # *exactly* one more key.
    def compute_next_states(state):
        positions, inventory = state
        for key, i in key_to_index.items():
            if key in inventory:
                continue
            pos = positions[i]
            if not inventory.issuperset(key_objects[pos][key]):
                continue
            new_positions = tuple(positions[:i] + (key,) + positions[i+1:])
            new_inventory = inventory.union(key)
            new_state = (new_positions, new_inventory)
            yield (new_state, key_distances[pos][key])

    # Initial state is the starting positions and an empty inventory.
    initial_state = (tuple(range(start_count)), frozenset())

    return initial_state, compute_next_states, len(key_to_index)

def compute_shortest_steps_bfs(initial_state, compute_next_states, key_count):
    curr_states = {initial_state: 0}
    for i in range(key_count):
        next_states = {}
        for state, cost in curr_states.items():
            for next_state, next_cost in compute_next_states(state):
                total_next_cost = cost + next_cost
                if next_state not in next_states or total_next_cost < next_states[next_state]:
                    next_states[next_state] = total_next_cost
        curr_states = next_states

    return min(curr_states.values())

def compute_shortest_steps_dfs(initial_state, compute_next_states, _):
    cache = {}
    def do_dfs_cached(state):
        if state in cache:
            return cache[state]

        res = do_dfs(state)
        cache[state] = res
        return res

    def do_dfs(state):
        return min((next_cost + do_dfs_cached(next_state) for next_state, next_cost in compute_next_states(state)), default=0)

    return do_dfs(initial_state)

def compute_shortest_steps_dijkstra(initial_state, compute_next_states, key_count):
    for state, _, dist in dijkstra_edges(initial_state, compute_next_states):
        if len(state[1]) == key_count:
            return dist

def change_to_part2(input):
    def _make_change(lines):
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

    lines = [[c for c in line.strip()] for line in input.strip().split('\n')]
    _make_change(lines)
    return '\n'.join(''.join(line) for line in lines)

def compute_day18(input):
    args1 = None
    def parse_input_part1():
        nonlocal args1
        args1 = parse_map(input, 1)

    parse_input1_duration = timeit.timeit(parse_input_part1, number=1)
    print(f'input parsing (part1) ({parse_input1_duration:.2f}s)')

    part1_bfs = None
    def do_part1_bfs():
        nonlocal part1_bfs
        part1_bfs = compute_shortest_steps_bfs(*args1)

    part1_bfs_duration = timeit.timeit(do_part1_bfs, number=1)
    print(f'part1 (bfs): {part1_bfs} ({part1_bfs_duration:.2f}s)')

    part1_dfs = None
    def do_part1_dfs():
        nonlocal part1_dfs
        part1_dfs = compute_shortest_steps_dfs(*args1)

    part1_dfs_duration = timeit.timeit(do_part1_dfs, number=1)
    print(f'part1 (dfs): {part1_dfs} ({part1_dfs_duration:.2f}s)')

    part1_dijkstra = None
    def do_part1_dijkstra():
        nonlocal part1_dijkstra
        part1_dijkstra = compute_shortest_steps_dijkstra(*args1)

    part1_dijkstra_duration = timeit.timeit(do_part1_dijkstra, number=1)
    print(f'part1 (dijkstra): {part1_dijkstra} ({part1_dijkstra_duration:.2f}s)')

    args2 = None
    def parse_input_part2():
        nonlocal args2
        input_part2 = change_to_part2(input)
        args2 = parse_map(input_part2, 4)

    parse_input2_duration = timeit.timeit(parse_input_part2, number=1)
    print(f'input parsing (part2) ({parse_input2_duration:.2f}s)')

    part2_bfs = None
    def do_part2_bfs():
        nonlocal part2_bfs
        part2_bfs = compute_shortest_steps_bfs(*args2)

    part2_bfs_duration = timeit.timeit(do_part2_bfs, number=1)

    print(f'part2 (bfs): {part2_bfs} ({part2_bfs_duration:.2f}s)')

    part2_dfs = None
    def do_part2_dfs():
        nonlocal part2_dfs
        part2_dfs = compute_shortest_steps_dfs(*args2)

    part2_dfs_duration = timeit.timeit(do_part2_dfs, number=1)

    print(f'part2 (dfs): {part2_dfs} ({part2_dfs_duration:.2f}s)')

    part2_dijkstra = None
    def do_part2_dijkstra():
        nonlocal part2_dijkstra
        part2_dijkstra = compute_shortest_steps_dijkstra(*args2)

    part2_dijkstra_duration = timeit.timeit(do_part2_dijkstra, number=1)

    print(f'part2 (dijkstra): {part2_dijkstra} ({part2_dijkstra_duration:.2f}s)')

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        compute_day18(input)
