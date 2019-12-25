from util import *
from graph import *
from heapq import heappush, heappop
import timeit
import networkx as nx
from itertools import count
from more_itertools import collapse

def get_label(lines, p):
    x0, y0 = p

    # Left
    if 'A' <= lines[y0][x0 - 1] <= 'Z':
        return lines[y0][x0-2:x0]

    # Right
    if 'A' <= lines[y0][x0 + 1] <= 'Z':
        return lines[y0][x0+1:x0+3]

    # Up
    if 'A' <= lines[y0 - 1][x0] <= 'Z':
        return lines[y0 - 2][x0] + lines[y0 - 1][x0]

    # Down
    if 'A' <= lines[y0 + 1][x0] <= 'Z':
        return lines[y0 + 1][x0] + lines[y0 + 2][x0]

    return None

def get_dz(lines, p):
    x0, y0 = p
    return -1 if x0 == 2 or x0 == len(lines[y0])-3 or y0 == 2 or y0 == len(lines) - 3 else +1

def parse_input(input):
    lines = [x for x in input.split('\n')][:-1]
    rows = len(lines)
    cols = len(lines[0])

    start_pos = None
    walkables = set()
    end_pos = None

    label_to_portals = {}

    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            p = (x, y)
            if c == '.':
                walkables.add(p)
                label = get_label(lines, p)
                if label is None:
                    continue

                if label == 'AA':
                    start_pos = p
                elif label == 'ZZ':
                    end_pos = p
                else:
                    if label in label_to_portals:
                        if len(label_to_portals[label]) > 2:
                            raise Exception(f'too many {label} {label_to_portals[label]}')
                        label_to_portals[label].add(p)
                    else:
                        label_to_portals[label] = set([p])

    if start_pos is None or end_pos is None:
        raise

    bad_labels = [(label, ps) for label, ps in label_to_portals.items() if len(ps) != 2]
    if bad_labels:
        raise Exception(f'{bad_labels}')

    portals = {}
    for p, q in label_to_portals.values():
        pdz = get_dz(lines, p)
        qdz = get_dz(lines, q)
        portals[p] = (q, pdz)
        portals[q] = (p, qdz)

    return walkables, start_pos, end_pos, portals

def local_neighbors(n, walkables):
    return [m for m in dir_neighbors(n) if m in walkables]

def compute_part1(walkables, start_pos, end_pos, portals):
    def neighbors(n):
        yield from local_neighbors(n, walkables)
        if n in portals:
            yield portals[n][0]

    return bidirectional_shortest_path_length(start_pos, end_pos, neighbors, neighbors)

def compute_local_graph(walkables):
    return nx.Graph([(n, m) for n in walkables for m in local_neighbors(n, walkables)])

def compute_part1_nx(walkables, start_pos, end_pos, portals):
    G = compute_local_graph(walkables)
    G.add_edges_from((n, m) for n, (m, _) in portals.items())
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

def tuple3to2(v3):
    return (v3[0], v3[1]), v3[2]

def tuple2to3(v2, z):
    return (v2[0], v2[1], z)

def compute_part2(walkables, start_pos, end_pos, portals):
    local = compute_local_graph(walkables)

    G = nx.Graph()

    labeled_nodes = [ start_pos, end_pos ] + list(portals.keys())
    for source in labeled_nodes:
        local_lengths = nx.shortest_path_length(local, source)
        for target in labeled_nodes:
            if target != source and target in local_lengths:
                G.add_edge(source, target, weight=local_lengths[target])

    start_pos3 = tuple2to3(start_pos, 0)
    end_pos3 = tuple2to3(end_pos, 0)

    def weighted_neighbors(n3):
        n, z = tuple3to2(n3)
        for m in G[n]:
            yield tuple2to3(m, z), G.edges[n, m]['weight']
        if n in portals:
            other_side, dz = portals[n]
            new_z = z + dz
            if new_z >= 0:
                yield tuple2to3(other_side, new_z), 1

    def heuristic(n3):
        return 0

    return bidirectional_dijkstra_shortest_path_length(start_pos3, end_pos3, weighted_neighbors, weighted_neighbors)

if __name__ == '__main__':
    with open('day20.input', 'r') as input_file:
        input = input_file.read()
        args = parse_input(input)

        part1 = None
        def do_part1():
            global part1
            part1 = compute_part1(*args)

        part1_nx = None
        def do_part1_nx():
            global part1_nx
            part1_nx = compute_part1_nx(*args)

        part2 = None
        def do_part2():
            global part2
            part2 = compute_part2(*args)

        part1_duration = timeit.timeit(do_part1, number=1)
        part1_nx_duration = timeit.timeit(do_part1_nx, number=1)
        part2_duration = timeit.timeit(do_part2, number=1)
        if part1 != part1_nx:
            raise Exception(f'computed {part1} for part 1, but NetworkX computed {part1_nx}')
        print(f'part1: {part1} ({part1_duration:.3f}s, nx={part1_nx_duration:.3f}s), part2: {part2} ({part2_duration:.3f}s)')

