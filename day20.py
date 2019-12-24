from util import *
from vec2 import *
from vec3 import *
import networkx as nx
from more_itertools import collapse

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

    counts = {start_pos: 0}

    def neighbors_part1(n):
        possible_neighbors = [n + d.vec() for d in all_directions]
        yield from (m for m in possible_neighbors if m in walkables)
        res = get_label(lines, n)
        if res and res[0] in portals:
            other_side = next(iter(portals[res[0]] - set([n])))
            yield other_side

    G = nx.Graph()
    for parent, child in bfs_edges(start_pos, neighbors_part1):
        counts[child] = counts[parent] + 1
        if has_direction(child - parent):
            G.add_edge(parent, child)

    part1 = counts[end_pos]

    H = nx.Graph()
    labeled_nodes = {
        start_pos: frozenset(['A']),
        end_pos: frozenset(['Z']),
    }
    for label, ends in portals.items():
        for end in ends:
            labeled_nodes[end] = label

    for source, label in labeled_nodes.items():
        H.add_node(source, label=label)
        lengths = nx.shortest_path_length(G, source)
        for target in labeled_nodes.keys():
            if target != source and target in lengths:
                H.add_edge(source, target, weight=lengths[target])

    start_pos3 = vec2to3(start_pos, 0)
    end_pos3 = vec2to3(end_pos, 0)

    counts3 = {start_pos3: 0}

    def neighbors_part2(n3):
        n, z = vec3to2(n3)
        possible_neighbors = [n + d.vec() for d in all_directions]
        yield from (vec2to3(m, z) for m in possible_neighbors if m in walkables)
        res = get_label(lines, n)
        if res and res[0] in portals:
            other_side = next(iter(portals[res[0]] - set([n])))
            new_z = z + res[1]
            if new_z >= 0:
                yield vec2to3(other_side, new_z)

    for parent, child in bfs_edges(start_pos3, neighbors_part2):
        counts3[child] = counts3[parent] + 1
        if child == end_pos3:
            break

    part2 = counts3[end_pos3]

    return part1, part2

if __name__ == '__main__':
    with open('day20.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day20(input)
        print(f'part1: {part1}, part2: {part2}')
