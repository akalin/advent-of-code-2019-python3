from util import *
from vec2 import *
from vec3 import *
import timeit
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

def parse_input(input):
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

    portal_sides = {}
    for x, y in portals.values():
        _, xdz = get_label(lines, x)
        _, ydz = get_label(lines, y)
        portal_sides[x] = (y, xdz)
        portal_sides[y] = (x, ydz)

    return walkables, start_pos, end_pos, portals, portal_sides

def vec3to2(v3):
    return Vec2(v3[0], v3[1]), v3[2]

def vec2to3(v2, z):
    return Vec3(v2[0], v2[1], z)

def local_neighbors(n, walkables):
    possible_neighbors = [n + d.vec() for d in all_directions]
    return (m for m in possible_neighbors if m in walkables)

def compute_part1(walkables, start_pos, end_pos, portals, portal_sides):
    counts = {start_pos: 0}

    def neighbors_part1(n):
        yield from local_neighbors(n, walkables)
        if n in portal_sides:
            yield portal_sides[n][0]

    for parent, child in bfs_edges(start_pos, neighbors_part1):
        counts[child] = counts[parent] + 1

    return counts[end_pos]

def compute_local_graph(walkables):
    return nx.Graph([(n, m) for n in walkables for m in local_neighbors(n, walkables)])

def compute_part1_nx(walkables, start_pos, end_pos, portals, portal_sides):
    G = compute_local_graph(walkables)
    G.add_edges_from((n, m) for n, (m, _) in portal_sides.items())
    return nx.shortest_path_length(G, source=start_pos, target=end_pos)

def compute_part2(walkables, start_pos, end_pos, portals, portal_sides):
    G = compute_local_graph(walkables)

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
#        print('n3', n3, labeled_nodes[n])
        for m in H[n]:
#            print('m', m, labeled_nodes[m])
            yield vec2to3(m, z)
#        print('n label', res)
        if n in portal_sides:
            other_side, dz = portal_sides[n]
            new_z = z + dz
            if new_z >= 0:
#                print('mos', other_side, labeled_nodes[other_side])
                yield vec2to3(other_side, new_z)

    for parent3, child3 in bfs_edges(start_pos3, neighbors_part2):
        parent, zp = vec3to2(parent3)
        child, zc = vec3to2(child3)
#        print(labeled_nodes[parent], zp, labeled_nodes[child], zc)
        if zp == zc:
            counts3[child3] = counts3[parent3] + H.edges[parent, child]['weight']
        else:
            counts3[child3] = counts3[parent3] + 1
        if child3 == end_pos3:
            break

    return counts3[end_pos3]

if __name__ == '__main__':
    with open('day20.input', 'r') as input_file:
        input = input_file.read()
        walkables, start_pos, end_pos, portals, portal_sides = parse_input(input)

        part1 = None
        def do_part1():
            global part1
            part1 = compute_part1(walkables, start_pos, end_pos, portals, portal_sides)

        part1_nx = None
        def do_part1_nx():
            global part1_nx
            part1_nx = compute_part1_nx(walkables, start_pos, end_pos, portals, portal_sides)

        part2 = None
        def do_part2():
            global part2
            part2 = compute_part2(walkables, start_pos, end_pos, portals, portal_sides)

        part1_duration = timeit.timeit(do_part1, number=1)
        part1_nx_duration = timeit.timeit(do_part1_nx, number=1)
        part2_duration = timeit.timeit(do_part2, number=1)
        if part1 != part1_nx:
            raise Exception(f'computed {part1} for part 1, but NetworkX computed {part1_nx}')
        print(f'part1: {part1} ({part1_duration:.2f}s, nx={part1_nx_duration:.2f}s), part2: {part2} ({part2_duration:.2f}s)')

