from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *
from vec3 import *

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

def get_label(lines, p):
    rows = len(lines)
    cols = len(lines[0])
    for d in all_directions:
        x1, y1 = p + d.vec()
        ch1 = lines[y1][x1]
        if 'A' <= ch1 <= 'Z':
            x2, y2 = Vec2(x1, y1) + d.vec()
            ch2 = lines[y2][x2]
            s = frozenset([ch1, ch2])
            if x2 == 0 or x2 == cols-1 or y2 == 0 or y2 == rows-1:
                return s, -1
            return s, +1
    return None

def vec3to2(v3):
    return Vec2(v3[0], v3[1]), v3[2]

def vec2to3(v2, z):
    return Vec3(v2[0], v2[1], z)

def compute_day20(input):
    lines = [x for x in input.split('\n')][:-1]
    rows = len(lines)
    cols = len(lines[0])

    start_pos = None
    walkables = set()
    end_pos = None

    portals = {}

    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            p = Vec2(x, y)
            if c == '.':
                walkables.add(p)
                res = get_label(lines, p)
                if res is None:
                    continue

                label = res[0]
                if label == frozenset(['A']):
                    start_pos = p
                elif label == frozenset(['Z']):
                    end_pos = p
                else:
                    if label in portals:
                        if len(portals[label]) > 2:
                            raise Exception(f'too many {label} {portals[label]}')
                        portals[label].add(p)
                    else:
                        portals[label] = set([p])

    if start_pos is None or end_pos is None:
        raise

    bad_labels = [v for v in portals.values() if len(v) != 2]
    if bad_labels:
        raise Exception(f'{bad_labels}')

    start_pos3 = vec2to3(start_pos, 0)
    end_pos3 = vec2to3(end_pos, 0)

    counts = {start_pos3: 0}

    def visit_fn(n, parent):
        counts[n] = counts[parent] + 1

    def get_neighbor_fn(n3):
        n, z = vec3to2(n3)
        if n not in walkables:
            return []
        possible_neighbors = [n + d.vec() for d in all_directions]
        neighbors = [vec2to3(m, z) for m in possible_neighbors if m in walkables]
        res = get_label(lines, n)
        if res and res[0] in portals:
            other_side = next(iter(portals[label] - set([n])))
            new_z = z + res[1]
            if new_z >= 0:
                neighbors.append(vec2to3(other_side, new_z))
        return neighbors

    do_bfs(start_pos3, get_neighbor_fn, visit_fn)

    return counts[end_pos3], None

if __name__ == '__main__':
    with open('day20.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day20(input)
        print(f'part1: {part1}, part2: {part2}')
