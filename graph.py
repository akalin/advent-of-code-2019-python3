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
    if source == target:
        return 0

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
    # See slides 9 and 10 of
    # https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/EPP%20shortest%20path%20algorithms.pdf
    # for a discussion of the stopping condition.
    shortest_length = None
    while fringe[0] and fringe[1]:
        (d, _, v) = heappop(fringe[dir])
        if shortest_length is not None and d + fringe[1 - dir][0][0] >= shortest_length:
            return shortest_length
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
                if u in seen[0] and u in seen[1]:
                    length = seen[0][u] + seen[1][u]
                    if shortest_length is None or length < shortest_length:
                        shortest_length = length
        dir = 1 - dir

    raise ValueError(f'No path between {source} and {target}')

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
            return g_score[target]

        for m, m_len in get_neighbor_fn(n):
            if n not in g_score:
                continue

            tentative_g_score = g_score[n] + m_len
            if (0, tentative_g_score) < get_g_score(m):
                came_from[m] = n
                g_score[m] = tentative_g_score
                f_score[m] = g_score[m] + h(m)
                heappush(open_set, (f_score[m], next(c), m))

    raise ValueError(f'No path between {source} and {target}')
