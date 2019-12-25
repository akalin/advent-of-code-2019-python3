from collections import deque
from heapq import heappush, heappop
from itertools import count

# Roughly equivalent to generic_bfs_edges from
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/traversal/breadth_first_search.html .
def bfs_edges(source, successors):
    visited = set([source])
    queue = deque([source])
    while queue:
        parent = queue.popleft()
        for child in successors(parent):
            if child not in visited:
                visited.add(child)
                yield parent, child
                queue.append(child)

def bfs_path_lengths(source, successors):
    lengths = {source: 0}
    queue = deque([source])
    yield source, 0
    while queue:
        parent = queue.popleft()
        for child in successors(parent):
            if child not in lengths:
                lengths[child] = lengths[parent] + 1
                yield child, lengths[child]
                queue.append(child)

def bidirectional_shortest_path_length(source, target, successors, predecessors):
    if source == target:
        return 0

    source_lengths = {source: 0}
    target_lengths = {target: 0}

    forward_fringe = [source]
    reverse_fringe = [target]

    while forward_fringe and reverse_fringe:
        if len(forward_fringe) <= len(reverse_fringe):
            this_level = forward_fringe
            fringe = forward_fringe = []
            neighbors = successors
            lengths, other_lengths = source_lengths, target_lengths
        else:
            this_level = reverse_fringe
            fringe = reverse_fringe = []
            neighbors = predecessors
            lengths, other_lengths = target_lengths, source_lengths
            
        for v in this_level:
            for w in neighbors(v):
                if w not in lengths:
                    fringe.append(w)
                    lengths[w] = lengths[v] + 1
                if w in other_lengths: # path found
                    return lengths[w] + other_lengths[w]

    raise Exception(f'No path between {source} and {target}')

# Adapted from _dijkstra_multisource in
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html .
def dijkstra_path_length(source, target, weighted_successors):
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

    raise ValueError(f'No path between {source} and {target}')

# Adapted from bidirectional_dijkstra in
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html#bidirectional_dijkstra .
def bidirectional_dijkstra_path_length(source, target, weighted_successors, weighted_predecessors):
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
