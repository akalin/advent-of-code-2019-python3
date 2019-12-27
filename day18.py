from graph import *
from itertools import chain
from util import *
import timeit
import networkx as nx

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

    local = nx.Graph([(n, m) for n in walkables for m in dir_neighbors(n) if m in walkables])

    key_distances = {}
    routes = {}

    for source, source_pos in chain(enumerate(start_positions), key_to_pos.items()):
        # We assume there's only one shortest path to source (i.e.,
        # not another one that may avoid doors).
        dists = {source_pos: 0}
        pos_routes = {source_pos: ''}
        for parent, child in bfs_edges(source_pos, neighbors):
            dists[child] = dists[parent] + 1
            pos_routes[child] = pos_routes[parent]
            if child in pos_to_door:
                pos_routes[child] += pos_to_door[child]
            elif child in pos_to_key:
                pos_routes[child] += pos_to_key[child]

        key_distances[source] = {target: dists[target_pos] for target, target_pos in key_to_pos.items() if target_pos in dists}
        routes[source] = {target: pos_routes[target_pos][:-1] for target, target_pos in key_to_pos.items() if target_pos in pos_routes}

    all_keys = frozenset(key_to_pos.keys())

    key_to_index = {}
    for key in all_keys:
        for i in range(start_count):
            if key in key_distances[i]:
                key_to_index[key] = i

    return start_count, key_distances, routes, all_keys, key_to_index

def compute_next_states(key_distances, routes, all_keys, key_to_index, state):
    positions, inventory = state
    for key in all_keys:
        if key in inventory:
            continue
        i = key_to_index[key]
        pos = positions[i]
        reachable = all(c in inventory or c.lower() in inventory for c in routes[pos][key])
        if reachable:
            new_positions = tuple(positions[:i] + (key,) + positions[i+1:])
            new_inventory = inventory | frozenset((key,))
            new_state = (new_positions, new_inventory)
            yield (new_state, key_distances[pos][key])

def compute_shortest_steps_bfs(start_count, key_distances, routes, all_keys, key_to_index):
    curr_states = {(tuple(range(start_count)), frozenset()): 0}
    for i in range(len(all_keys)):
        next_states = {}
        for state, cost in curr_states.items():
            for next_state, next_cost in compute_next_states(key_distances, routes, all_keys, key_to_index, state):
                total_next_cost = cost + next_cost
                if next_state not in next_states or total_next_cost < next_states[next_state]:
                    next_states[next_state] = total_next_cost
        curr_states = next_states

    return min(curr_states.values())

def compute_shortest_steps_dfs(start_count, key_distances, routes, all_keys, key_to_index):
    cache = {}
    def do_dfs_cached(state):
        if state in cache:
            return cache[state]

        res = do_dfs(state)
        cache[state] = res
        return res

    def do_dfs(state):
        return min((next_cost + do_dfs_cached(next_state) for next_state, next_cost in compute_next_states(key_distances, routes, all_keys, key_to_index, state)), default=0)

    return do_dfs((tuple(range(start_count)), frozenset()))

def compute_shortest_steps_dijkstra(start_count, key_distances, routes, all_keys, key_to_index):
    start_state = (tuple(range(start_count)), frozenset())
    def weighted_successors(state):
        return compute_next_states(key_distances, routes, all_keys, key_to_index, state)

    for state, _, dist in dijkstra_edges(start_state, weighted_successors):
        if len(state[1]) == len(all_keys):
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
    args2 = None
    def parse_input():
        nonlocal args1, args2
        args1 = parse_map(input, 1)
        input_part2 = change_to_part2(input)
        args2 = parse_map(input_part2, 4)

    parse_input_duration = timeit.timeit(parse_input, number=1)
    print(f'input parsing ({parse_input_duration:.2f}s)')

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
