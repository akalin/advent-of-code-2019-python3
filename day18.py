from util import *
from heapq import heappush, heappop
from itertools import count
import networkx as nx

def dijkstra_path_length_fn(source, is_target, weighted_successors):
    dist = {}
    seen = {source: 0}
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    fringe = []
    heappush(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = heappop(fringe)
        if is_target(v):
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

    raise ValueError(f'No path between {source} and {target}')

def compute_day18(input):
    input = '''
#########
#b.A.@.a#
#########
'''
    lines = [x.strip() for x in input.strip().split('\n')]
    rows = len(lines)
    cols = len(lines[0])

    start_pos = None
    pos_to_key = {}
    key_to_pos = {}
    pos_to_door = {}
    door_to_pos = {}
    walkables = set()

    for y in range(rows):
        for x in range(cols):
            c = lines[y][x]
            if c == '#':
                continue
            p = (x, y)
            if c == '@':
                start_pos = p
            elif c == '.':
                pass
            elif 'a' <= c <= 'z':
                pos_to_key[p] = c
                key_to_pos[c] = p
            elif 'A' <= c <= 'Z':
                pos_to_door[p] = c
                door_to_pos[c] = p
            else:
                raise

            walkables.add(p)

    if start_pos is None:
        raise

    def local_neighbors(n, walkables):
        return [m for m in dir_neighbors(n) if m in walkables]

    local = nx.Graph([(n, m) for n in walkables for m in local_neighbors(n, walkables)])

    G = nx.Graph()

    labeled_nodes = [ start_pos ] + list(pos_to_key.keys())
    for source in labeled_nodes:
        local_lengths = nx.shortest_path_length(local, source)
        for target in labeled_nodes:
            if target != source and target in local_lengths:
                G.add_edge(source, target, weight=local_lengths[target])

    print(labeled_nodes, G.nodes, G.edges)

    def weighted_neighbors(state):
        pos, inventory = state
        for new_pos, attributes in G[pos].items():
            if new_pos == start_pos:
                continue
            new_inventory = inventory | frozenset([pos_to_key[new_pos]])
            new_state = (new_pos, new_inventory)
            yield (new_state, attributes['weight'])

    all_keys = frozenset(key_to_pos.keys())
    def is_target(state):
        return state[1] == all_keys

    start_state = (start_pos, frozenset())
    part1 = dijkstra_path_length_fn(start_state, is_target, weighted_neighbors)

    return part1, None

if __name__ == '__main__':
    with open('day18.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day18(input)
        print(f'part1: {part1}, part2: {part2}')
