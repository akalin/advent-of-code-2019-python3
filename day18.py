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

def do_a_star(start, get_neighbor_fn, h, is_goal):
    open_set = set([start])
    came_from = {start: None}

    g_score = {start: 0}
    f_score = {start: h(start)}

    def get_g_score(n):
        if n not in g_score:
            return (1, 0)
        return (0, g_score[n])

    def get_f_score(n):
        if n not in f_score:
            return (1, 0)
        return (0, f_score[n])

    while len(open_set) > 0:
        n = min(open_set, key=get_f_score)
        if is_goal(n):
            return g_score, f_score, came_from
        open_set.remove(n)

        for m, m_len in get_neighbor_fn(n):
            if n not in g_score:
                continue

            tentative_g_score = g_score[n] + m_len
            if (0, tentative_g_score) < get_g_score(m):
                came_from[m] = n
                g_score[m] = tentative_g_score
                f_score[m] = g_score[m] + h(m)
                open_set.add(m)

    return None

def compute_day18(input):
    input2 = '''
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
    input = '''
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

    def get_raw_dists(pos):
        dists = {pos: 0}
        blockers = {pos: frozenset()}
        key_dists = {}
        def get_neighbor_fn(n):
            if n in walls:
                return []
            possible_neighbors = [n + d.vec() for d in all_directions]
            return [m for m in possible_neighbors if (m not in walls)]

        def visit_fn(n, parent):
            dists[n] = dists[parent] + 1
            new_blockers = blockers[parent]
            if n in pos_to_door:
                new_blockers |= frozenset(pos_to_door[n])
            blockers[n] = new_blockers

        do_bfs(pos, get_neighbor_fn, visit_fn)

        return {k: (dists[p], blockers[p]) for k, p in key_to_pos.items()}

    dist_cache = {}
    def get_raw_dists_cached(pos):
        if pos in dist_cache:
            return dist_cache[pos]
        v = get_raw_dists(pos)
        print(f'computing for {pos}')
        dist_cache[pos] = v
        return v

    def get_dists(pos, inventory):
        key_info = get_raw_dists_cached(pos)
        v = {k: d for k, (d, b) in key_info.items() if inventory.issuperset([d.lower() for d in b]) and k not in inventory}
        return v

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

    def heuristic(n):
        pos, inventory = n
        key_dists = get_dists(pos, inventory)
        if len(key_dists) == 0:
            return 0
        return min(key_dists.values())

    all_keys = frozenset(key_to_pos.keys())
    def is_goal(n):
        return n[1] == all_keys

    dists, f_dists, prev = do_a_star(initial_state, get_neighbor_fn, heuristic, is_goal)
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
