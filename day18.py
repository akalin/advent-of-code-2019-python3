from graph import *
from itertools import chain
from util import *
import networkx as nx

def compute_shortest_steps(input, start_count):
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    start_positions = []
    key_to_pos = {}
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
            elif 'A' <= c <= 'Z':
                pos_to_door[p] = c
            else:
                raise

            walkables.add(p)

    if len(start_positions) != start_count:
        raise

    local = nx.Graph([(n, m) for n in walkables for m in dir_neighbors(n) if m in walkables])

    key_distances = {}
    blockers = {}

    for source, source_pos in chain(enumerate(start_positions), key_to_pos.items()):
        # We assume there's only one shortest path to source (i.e.,
        # not another one that may avoid doors).
        paths = nx.single_source_shortest_path(local, source_pos)
        key_distances[source] = {}
        blockers[source] = {}
        for target, target_pos in key_to_pos.items():
            if target_pos not in paths:
                continue
            blockers[source][target] = frozenset(pos_to_door[n].lower() for n in paths[target_pos][1:] if n in pos_to_door)
            key_distances[source][target] = len(paths[target_pos]) - 1

    all_keys = frozenset(key_to_pos.keys())

    key_to_index = {}
    for key in all_keys:
        for i in range(start_count):
            if key in key_distances[i]:
                key_to_index[key] = i

    def weighted_neighbors(state):
        positions, inventory = state
        for key in all_keys:
            if key in inventory:
                continue
            i = key_to_index[key]
            pos = positions[i]
            if inventory.issuperset(blockers[i][key]):
                new_positions = tuple(positions[:i] + (key,) + positions[i+1:])
                new_inventory = inventory | set((key,))
                new_state = (new_positions, new_inventory)
                yield (new_state, key_distances[pos][key])

    curr_states = {(tuple(range(start_count)), frozenset()): 0}
    for i in range(len(all_keys)):
        next_states = {}
        for state, cost in curr_states.items():
            for next_state, next_cost in weighted_neighbors(state):
                total_next_cost = cost + next_cost
                if next_state not in next_states or total_next_cost < next_states[next_state]:
                    next_states[next_state] = total_next_cost
        curr_states = next_states

    return min(curr_states.values())

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
