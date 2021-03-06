from collections import deque
from heapq import heappush, heappop
from itertools import count

# Roughly equivalent to generic_bfs_edges from
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/traversal/breadth_first_search.html .
def bfs_edges(source, successors):
    visited = {source}
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
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html and
# dijkstra_search in
# https://www.redblobgames.com/pathfinding/a-star/implementation.html .
def dijkstra_edges(source, weighted_successors):
    final_dist = {}
    dist_so_far = {source: 0}
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    fringe = []
    heappush(fringe, (0, next(c), source, None))
    while fringe:
        (_, _, child, parent) = heappop(fringe)
        if child in final_dist:
            continue # already processed this node

        dist_to_child = dist_so_far[child]
        final_dist[child] = dist_to_child
        yield child, parent, dist_to_child

        for grandchild, weight in weighted_successors(child):
            dist_to_grandchild = dist_to_child + weight
            if grandchild in final_dist:
                if dist_to_grandchild < final_dist[grandchild]:
                    raise ValueError(f'Contradictory paths found: negative weights? child={child} distance to {grandchild}={dist_to_child} + {weight} = {dist_to_grandchild} < final distance to {grandchild}={final_dist[grandchild]}')
            elif grandchild not in dist_so_far or dist_to_grandchild < dist_so_far[grandchild]:
                dist_so_far[grandchild] = dist_to_grandchild
                heappush(fringe, (dist_to_grandchild, next(c), grandchild, child))

# Adapted from _dijkstra_multisource in
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/weighted.html .
def dijkstra_path_length(source, target, weighted_successors):
    for child, _, dist_to_child in dijkstra_edges(source, weighted_successors):
        if child == target:
            return dist_to_child

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
    weighted_next = [weighted_successors, weighted_predecessors]
    # See slides 9 and 10 of
    # https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/EPP%20shortest%20path%20algorithms.pdf
    # for a discussion of the stopping condition.
    shortest_length = None
    while fringe[0] and fringe[1]:
        dir = 0 if len(fringe[0]) <= len(fringe[1]) else 1
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
                    raise ValueError(f'Contradictory paths found: negative weights? child={child} distance to {grandchild}={dist_to_child} + {weight} = {dist_to_grandchild} < final distance to {grandchild}={final_dist[grandchild]}')
            elif u not in seen[dir] or vu_dist < seen[dir][u]:
                seen[dir][u] = vu_dist
                heappush(fringe[dir], (vu_dist, next(c), u))
                if u in seen[0] and u in seen[1]:
                    length = seen[0][u] + seen[1][u]
                    if shortest_length is None or length < shortest_length:
                        shortest_length = length

    raise ValueError(f'No path between {source} and {target}')

def astar_edges(source, weighted_successors, heuristic):
    dist_so_far = {source: 0}
    # Use a counter to avoid comparing the nodes themselves in the
    # heap.
    c = count()
    fringe = []
    heappush(fringe, (0, next(c), source, None))
    while fringe:
        (_, _, child, parent) = heappop(fringe)

        dist_to_child = dist_so_far[child]
        # The yielded edges aren't necessarily optimal for child unless
        # child is the target of the heuristic
        yield child, parent, dist_to_child

        for grandchild, weight in weighted_successors(child):
            dist_to_grandchild = dist_to_child + weight
            if grandchild not in dist_so_far or dist_to_grandchild < dist_so_far[grandchild]:
                dist_so_far[grandchild] = dist_to_grandchild
                heappush(fringe, (dist_to_grandchild + heuristic(grandchild), next(c), grandchild, child))

def astar_path_length(source, target, weighted_successors, heuristic):
    for child, _, dist_to_child in astar_edges(source, weighted_successors, heuristic):
        if child == target:
            return dist_to_child

    raise ValueError(f'No path between {source} and {target}')
