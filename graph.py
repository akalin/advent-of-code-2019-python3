from collections import deque

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
