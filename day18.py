from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *

def do_bfs(start, get_neighbor_fn, visit_fn):
    visited = set([start])
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for m in get_neighbor_fn(n):
            if m not in visited:
                visited.add(m)
                visit_fn(m, n)
                queue.append(m)

def do_weighted_bfs(start, get_neighbor_fn, visit_fn):
    visited = set([start])
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for m in get_neighbor_fn(n):
            if m not in visited:
                visited.add(m)
                visit_fn(m, n)
                queue.append(m)

def compute_day18(input):
    input = '''
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
'''
#    input = '''
##########
##b.A.@.a#
##########
#'''
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    initial_pos = None
    pos_to_key = {}
    key_to_pos = {}
    pos_to_door = {}
    door_to_pos = {}
    walls = set()

    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            p = Vec2(x, y)
            if c == '@':
                initial_pos = p
            elif c == '#':
                walls.add(p)
            elif ord('a') <= ord(c) <= ord('z'):
                pos_to_key[p] = c
                key_to_pos[c] = p
            elif ord('A') <= ord(c) <= ord('Z'):
                pos_to_door[p] = c
                door_to_pos[c] = p

    if initial_pos is None:
        raise

    def get_dists(pos, inventory):
        def can_access(p):
            if p in walls:
                return False

            if p in pos_to_door:
                door = pos_to_door[p]
                key = door.lower()
                return (key in inventory)

            return True

        dists = {pos: 0}
        key_dists = {}
        def get_neighbor_fn(n):
            if not can_access(n):
                return []
            possible_neighbors = [n + d.vec() for d in all_directions]
            return [m for m in possible_neighbors if can_access(m)]

        def visit_fn(n, parent):
            dists[n] = dists[parent] + 1

            if n in pos_to_key:
                key_dists[pos_to_key[n]] = dists[n]

        do_bfs(pos, get_neighbor_fn, visit_fn)
        return (key_dists)

    initial_state = (initial_pos, ())

    dists = {initial_state: 0}

    dist_cache = {}

    def get_neighbor_fn(n):
        pos, inventory = n
        key_dists = get_dists(pos, inventory)
        neighbors = []
        for k, dist in key_dists.items():
            if k in inventory:
                continue
            new_pos = key_to_pos[k]
            new_inventory = list(inventory)
            new_inventory.append(k)
            new_state = (new_pos, tuple(new_inventory))
            neighbors.append(new_state)
            dist_cache[new_state] = dist
        return neighbors

    def visit_fn(n, parent):
        pos, inventory = n
        if n not in dists:
            dists[n] = dists[parent] + dist_cache[n]
            print(f'visiting {n} dist={dists[parent]} + {dist_cache[n]}')

    do_bfs(initial_state, get_neighbor_fn, visit_fn)
    all_keys = frozenset(key_to_pos.keys())
    final_states = [(state[1], dist) for (state, dist) in dists.items() if frozenset(state[1]) == all_keys]
    print(min(final_states))

    return None, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
