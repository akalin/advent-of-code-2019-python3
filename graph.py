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

def bidirectional_shortest_path_helper(source, target, successors, predecessors):
    pred = {source: None}
    succ = {target: None}

    if source == target:
        return (pred, succ, source)

    forward_fringe = [source]
    reverse_fringe = [target]

    while forward_fringe and reverse_fringe:
        if len(forward_fringe) <= len(reverse_fringe):
            this_level = forward_fringe
            forward_fringe = []
            for v in this_level:
                for w in successors(v):
                    if w not in pred:
                        forward_fringe.append(w)
                        pred[w] = v
                    if w in succ: # path found
                        return pred, succ, w
        else:
            this_level = reverse_fringe
            reverse_fringe = []
            for v in this_level:
                for w in predecessors(v):
                    if w not in succ:
                        reverse_fringe.append(w)
                        succ[w] = v
                    if w in pred: # path found
                        return pred, succ, w

    raise Exception(f'No path between {source} and {target}')

def bidirectional_shortest_path_length(source, target, successors, predecessors):
    pred, succ, w = bidirectional_shortest_path_helper(source, target, successors, predecessors)

    length = 0

    v = pred[w]
    while v is not None:
        length += 1
        v = pred[v]

    v = succ[w]
    while v is not None:
        length += 1
        v = succ[v]

    return length
