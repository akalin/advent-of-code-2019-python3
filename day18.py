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

def compute_day18(input):
    lines = input.strip().split('\n')
    rows = len(lines)
    cols = len(lines[0])

    pos = None
    keys = {}
    doors = {}
    walls = set()

    for y in range(rows):
        for x in range(cols):
            c = lines[x][y]
            p = Vec2(x, y)
            if c == '@':
                pos = p
            elif c == '#':
                walls.add(p)
            elif ord('a') <= ord(c) <= ord('z'):
                keys[p] = c
            elif ord('A') <= ord(c) <= ord('Z'):
                doors[p] = c

    if pos is None:
        raise

    dists = {pos: 0}
    key_dists = {}
    door_dists = {}
    def get_neighbor_fn(n):
        if n in walls:
            return []
        possible_neighbors = [n + d.vec() for d in all_directions]
        return [m for m in possible_neighbors if (m not in walls)]

    def visit_fn(n, parent):
        dists[n] = dists[parent] + 1

        if n in keys:
            key_dists[keys[n]] = dists[n]
        elif n in doors:
            door_dists[doors[n]] = dists[n]

    do_bfs(pos, get_neighbor_fn, visit_fn)

    print(key_dists, door_dists)

    return None, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
