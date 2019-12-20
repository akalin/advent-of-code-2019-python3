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

def get_label(lines, p):
    for d in all_directions:
        x1, y1 = p + d.vec()
        ch1 = lines[y1][x1]
        if 'A' <= ch1 <= 'Z':
            x2, y2 = Vec2(x1, y1) + d.vec()
            ch2 = lines[y2][x2]
            return frozenset([ch1, ch2])
    return None

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
                label = get_label(lines, p)
                if label is None:
                    continue

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

    counts = {start_pos: 0}

    def visit_fn(n, parent):
        counts[n] = counts[parent] + 1

    def get_neighbor_fn(n):
        if n not in walkables:
            return []
        possible_neighbors = [n + d.vec() for d in all_directions]
        neighbors = [m for m in possible_neighbors if m in walkables]
        label = get_label(lines, n)
        if label in portals:
            other_side = next(iter(portals[label] - set([n])))
            neighbors.append(other_side)
        return neighbors

    do_bfs(start_pos, get_neighbor_fn, visit_fn)

    return counts[end_pos], None

if __name__ == '__main__':
    with open('day20.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day20(input)
        print(f'part1: {part1}, part2: {part2}')
