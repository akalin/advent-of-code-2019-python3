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
            forward_fringe = []
            for v in this_level:
                for w in successors(v):
                    if w not in source_lengths:
                        forward_fringe.append(w)
                        source_lengths[w] = source_lengths[v] + 1
                    if w in target_lengths: # path found
                        return source_lengths[w] + target_lengths[w]
        else:
            this_level = reverse_fringe
            reverse_fringe = []
            for v in this_level:
                for w in predecessors(v):
                    if w not in target_lengths:
                        reverse_fringe.append(w)
                        target_lengths[w] = target_lengths[v] + 1
                    if w in source_lengths: # path found
                        return source_lengths[w] + target_lengths[w]

    raise Exception(f'No path between {source} and {target}')
