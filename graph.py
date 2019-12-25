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
                yield parent, child
                visited.add(child)
                queue.append(child)

def bfs_distances(source, successors):
    distances = {source: 0}
    for parent, child in bfs_edges(source, successors):
        distances[child] = distances[parent] + 1
    return distances
