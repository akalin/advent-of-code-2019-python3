from intcode import *
from util import *
from vec2 import *
import networkx as nx

def compute_day15(input):
    program = parse_intcode(input)

    walls = set()
    oxygen = None
    origin = Vec2(0, 0)

    dir_to_input = {
        'U': 1,
        'R': 4,
        'D': 2,
        'L': 3,
    }

    def show_map(pos=None):
        canvas = ASCIICanvas()
        canvas.put_set(walls, '.')
        canvas.put(origin, 'o')
        if oxygen:
            canvas.put(oxygen, 'O')
        if pos:
            canvas.put(pos, '*')
        cls()
        print(canvas.render(flip_y=True))

    intputers = {origin: Intputer(program)}
    origin_distances = {origin: 0}

    def neighbors(n):
        if n in walls:
            return []
        possible_neighbors = [n + d.vec() for d in all_directions]
        return (m for m in possible_neighbors if (m not in walls))

    G = nx.Graph()

    for parent, child in bfs_edges(origin, neighbors):
        intputer = intputers[parent].copy()
        dir = Direction(child - parent)
        input = dir_to_input[dir.str()]
        output = intputer.run([input])
        status = output[0]
        if status == 0:
            walls.add(child)
        elif status == 1:
            pass
        elif status == 2:
            oxygen = child
        else:
            raise Exception(f'unknown status {status}')

        if status != 0:
            G.add_edge(parent, child)
            intputers[child] = intputer
            origin_distances[child] = origin_distances[parent] + 1

    # show_map()

    if oxygen is None:
        raise Exception('oxygen not found')

    part1 = origin_distances[oxygen]
    part1_nx = nx.shortest_path_length(G, source=origin, target=oxygen)
    if part1 != part1_nx:
        raise Exception(f'computed {part1} for part 1, but NetworkX computed {part1_nx}')

    oxygen_distances = {oxygen: 0}

    for parent, child in bfs_edges(oxygen, neighbors):
        oxygen_distances[child] = oxygen_distances[parent] + 1

    part2 = max(oxygen_distances.values())

    part2_nx = max(nx.shortest_path_length(G, oxygen).values())
    if part2 != part2_nx:
        raise Exception(f'computed {part2} for part 2, but NetworkX computed {part2_nx}')

    return part1, part2

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2: {part2}')
