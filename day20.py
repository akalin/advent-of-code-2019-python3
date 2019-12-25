from util import *
from vec2 import *
from vec3 import *
from graph import *
from heapq import heappush, heappop
import timeit
import networkx as nx
from itertools import count
from more_itertools import collapse

def get_label(lines, p):
    rows = len(lines)
    cols = len(lines[0])
    for d in all_directions:
        x1, y1 = d.vec() + p
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
            p = (x, y)
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

def local_neighbors(n, walkables):
    return (m for m in dir_neighbors(n) if m in walkables)

def compute_part1(walkables, start_pos, end_pos, portals, portal_sides):
    def neighbors(n):
        yield from local_neighbors(n, walkables)
        if n in portal_sides:
            yield portal_sides[n][0]

    return bidirectional_shortest_path_length(start_pos, end_pos, neighbors, neighbors)

def compute_local_graph(walkables):
    return nx.Graph([(n, m) for n in walkables for m in local_neighbors(n, walkables)])

def compute_part1_nx(walkables, start_pos, end_pos, portals, portal_sides):
    G = compute_local_graph(walkables)
    G.add_edges_from((n, m) for n, (m, _) in portal_sides.items())
    return nx.shortest_path_length(G, source=start_pos, target=end_pos)

# Adapted from _dijkstra_multisource in
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html .
def dijkstra_shortest_path_length(source, target, weighted_successors):
    dist = {}
    seen = {source: 0}
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    fringe = []
    heappush(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = heappop(fringe)
        if v == target:
            return d
        if v in dist:
            continue # already searched this node
        dist[v] = d
        for u, cost in weighted_successors(v):
            vu_dist = dist[v] + cost
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError(f'Contradictory paths found: negative weights? v={v} u={u} vu_dist={vu_dist} dist[u]={dist[u]}')
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                heappush(fringe, (vu_dist, next(c), u))

    raise Exception(f'No path between {source} and {target}')

# Adapted from bidirectional_dijkstra in
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html#bidirectional_dijkstra .
def bidirectional_dijkstra_shortest_path_length(source, target, weighted_successors, weighted_predecessors):
    dist = [{}, {}]
    seen = [{source: 0}, {target: 0}]
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    fringe = [[], []]
    heappush(fringe[0], (0, next(c), source))
    heappush(fringe[1], (0, next(c), target))
    dir = 0
    weighted_next = [weighted_successors, weighted_predecessors]
    while fringe[0] and fringe[1]:
        (d, _, v) = heappop(fringe[dir])
        if v in dist[1 - dir]:
            return d + dist[1 - dir][v]
        if v in dist[dir]:
            continue # already searched this node
        dist[dir][v] = d
        for u, cost in weighted_next[dir](v):
            vu_dist = dist[dir][v] + cost
            if u in dist[dir]:
                if vu_dist < dist[dir][u]:
                    raise ValueError(f'Contradictory paths found: negative weights? v={v} u={u} vu_dist={vu_dist} dist[{dir}][u]={dist[dir][u]}')
            elif u not in seen[dir] or vu_dist < seen[dir][u]:
                seen[dir][u] = vu_dist
                heappush(fringe[dir], (vu_dist, next(c), u))
        dir = 1 - dir

    raise Exception(f'No path between {source} and {target}')

def astar(source, target, get_neighbor_fn, h):
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    open_set = []
    heappush(open_set, (0, next(c), source))
    came_from = {source: None}

    g_score = {source: 0}
    f_score = {source: h(source)}

    def get_g_score(n):
        if n not in g_score:
            return (1, 0)
        return (0, g_score[n])

    def get_f_score(n):
        if n not in f_score:
            return (1, 0)
        return (0, f_score[n])

    while open_set:
        (_, _, n) = heappop(open_set)
        if n == target:
            return g_score

        for m, m_len in get_neighbor_fn(n):
            if n not in g_score:
                continue

            tentative_g_score = g_score[n] + m_len
            if (0, tentative_g_score) < get_g_score(m):
                came_from[m] = n
                g_score[m] = tentative_g_score
                f_score[m] = g_score[m] + h(m)
                heappush(open_set, (f_score[m], next(c), m))

    raise

def vec3to2(v3):
    return Vec2(v3[0], v3[1]), v3[2]

def vec2to3(v2, z):
    return Vec3(v2[0], v2[1], z)

def compute_part2(walkables, start_pos, end_pos, portals, portal_sides):
    local = compute_local_graph(walkables)

    G = nx.Graph()
    labeled_nodes = {
        start_pos: frozenset(['A']),
        end_pos: frozenset(['Z']),
    }
    for label, ends in portals.items():
        for end in ends:
            labeled_nodes[end] = label

    for source in labeled_nodes.keys():
        local_lengths = nx.shortest_path_length(local, source)
        for target in labeled_nodes.keys():
            if target != source and target in local_lengths:
                G.add_edge(source, target, weight=local_lengths[target])

    start_pos3 = vec2to3(start_pos, 0)
    end_pos3 = vec2to3(end_pos, 0)

    def weighted_neighbors(n3):
        n, z = vec3to2(n3)
        for m in G[n]:
            yield vec2to3(m, z), G.edges[n, m]['weight']
        if n in portal_sides:
            other_side, dz = portal_sides[n]
            new_z = z + dz
            if new_z >= 0:
                yield vec2to3(other_side, new_z), 1

    def heuristic(n3):
        return 0

    return bidirectional_dijkstra_shortest_path_length(start_pos3, end_pos3, weighted_neighbors, weighted_neighbors)

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

