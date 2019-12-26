from util import *
from graph import *
from heapq import heappush, heappop
import timeit
import networkx as nx
from itertools import count, combinations

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

def tuple3to2(v3):
    return (v3[0], v3[1]), v3[2]

def tuple2to3(v2, z):
    return (v2[0], v2[1], z)

def compute_part2(walkables, start_pos, end_pos, portals, path_length):
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

    return path_length(G, portals, start_pos3, end_pos3, weighted_neighbors, weighted_neighbors)

def dijkstra(G, portals, start, end, succ, pred):
    return dijkstra_path_length(start, end, succ)

def bidir_dijkstra(G, portals, start, end, succ, pred):
    return bidirectional_dijkstra_path_length(start, end, succ, pred)

def zero_heuristic(n):
    return 0

def astar_zero(G, portals, start, end, succ, pred):
    return astar_path_length(start, end, succ, zero_heuristic)

def astar(G, portals, start, end, succ, pred):
    up_nodes = [p for p, (_, dz) in portals.items() if dz > 0]
    down_nodes = [p for p, (_, dz) in portals.items() if dz < 0]

    # n -> minimum distance from n to an up portal
    min_to_up = {n: 0 if n in up_nodes else min((G[n][p]['weight'] for p in up_nodes if G.has_edge(n, p))) for n in G.nodes()}

    # n -> minimum distance from n to a down portal
    min_to_down = {n: 0 if n in down_nodes else min((G[n][p]['weight'] for p in down_nodes if G.has_edge(n, p))) for n in G.nodes()}

    # minimum distance from an up portal to a down portal
    min_up_to_down = min(min_to_down[p] for p in up_nodes)

    # minimum distance from a down portal to another down portal
    min_down_to_other_down = min(G[n][p]['weight'] for n, p in combinations(G.nodes(), 2) if G.has_edge(n, p))

    end2, _ = tuple3to2(end)

    def heuristic(n3):
        n, z = tuple3to2(n3)
        if z == 0:
            if n == end2:
                return 0
            if G.has_edge(n, end2):
                return G.edges[n, end2]['weight']
            # If we're on the ground floor and we don't have a direct
            # edge to end, then we at least have to go up, go to
            # another portal, come back down, and go to end.
            return min_to_up[n] + 1 + min_down_to_other_down + 1 + min_to_up[end2]
        else:
            # Otherwise, we have at least have to go to a down portal,
            # go to the ground floor, then go to end.
            return min_to_down[n] + (1 + min_up_to_down) * (z - 1) + 1 + min_to_up[end2]

    return astar_path_length(start, end, succ, heuristic)

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


        part2_dijkstra = None
        def do_part2_dijkstra():
            global part2_dijkstra
            part2_dijkstra = compute_part2(*args, dijkstra)

        part2_bidir_dijkstra = None
        def do_part2_bidir_dijkstra():
            global part2_bidir_dijkstra
            part2_bidir_dijkstra = compute_part2(*args, bidir_dijkstra)

        part2_astar_zero = None
        def do_part2_astar_zero():
            global part2_astar_zero
            part2_astar_zero = compute_part2(*args, astar_zero)

        part2_astar = None
        def do_part2_astar():
            global part2_astar
            part2_astar = compute_part2(*args, astar)

        part1_duration = timeit.timeit(do_part1, number=1)
        part1_nx_duration = timeit.timeit(do_part1_nx, number=1)
        part2_dijkstra_duration = timeit.timeit(do_part2_dijkstra, number=1)
        part2_bidir_dijkstra_duration = timeit.timeit(do_part2_bidir_dijkstra, number=1)
        part2_astar_zero_duration = timeit.timeit(do_part2_astar_zero, number=1)
        part2_astar_duration = timeit.timeit(do_part2_astar, number=1)
        if part1 != part1_nx:
            raise Exception(f'computed {part1} for part 1, but NetworkX computed {part1_nx}')
        print(f'part1: {part1} ({part1_duration:.3f}s, nx={part1_nx_duration:.3f}s)')
        print(f'part2 (dijkstra): {part2_dijkstra} ({part2_dijkstra_duration:.3f}s)')
        print(f'part2 (bidir dijkstra): {part2_bidir_dijkstra} ({part2_bidir_dijkstra_duration:.3f}s)')
        print(f'part2 (A* zero): {part2_astar_zero} ({part2_astar_zero_duration:.3f}s)')
        print(f'part2 (A*): {part2_astar} ({part2_astar_duration:.3f}s)')

