from collections import deque
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

def do_dijkstra(start, get_neighbor_fn):
    dist = {start: 0}
    prev = {start: None}

    def get_dist(n):
        if n not in dist:
            return (1, 0)
        return (0, dist[n])

    visited = set()
    queue = set([start])
    while len(queue) > 0:
        n = min(queue, key=get_dist)
        queue.remove(n)

        for m, m_len in get_neighbor_fn(n):
            if m in visited:
                continue
            queue.add(m)

            alt = dist[n] + m_len
            if (0, alt) < get_dist(m):
                dist[m] = alt
                prev[m] = n

        visited.add(n)

    return dist, prev

def compute_day18(input):
    input = '''
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
'''
    input2 = '''
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
'''
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

            if n in pos_to_key and pos_to_key[n] not in inventory:
                key_dists[pos_to_key[n]] = dists[n]

        do_bfs(pos, get_neighbor_fn, visit_fn)
        return (key_dists)

    initial_state = (initial_pos, frozenset())

    max_l = 0
    def get_neighbor_fn(n):
        nonlocal max_l
        pos, inventory = n
        if len(inventory) > max_l:
            print(max_l)
            max_l = len(inventory)
        key_dists = get_dists(pos, inventory)
        neighbors = []
        for k, dist in key_dists.items():
            new_pos = key_to_pos[k]
            new_inventory = inventory | frozenset([k])
            new_state = (new_pos, new_inventory)
            neighbors.append((new_state, dist))
        return neighbors

    all_keys = frozenset(key_to_pos.keys())
    dists, prev = do_dijkstra(initial_state, get_neighbor_fn)
#    for d in dists.items():
#        print(d)
#    for p in prev.items():
#        print(p)

#    do_bfs(initial_state, get_neighbor_fn, visit_fn)
    final_states = [(state[1], dist) for (state, dist) in dists.items() if frozenset(state[1]) == all_keys]
    print('min', min(final_states, key=lambda x: x[1]))

    return None, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
