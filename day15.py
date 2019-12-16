from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *

def do_bfs(start, get_neighbor_fn, visit_fn):
    visited = set([start])
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for m in get_neighbor_fn(n):
            if m not in visited:
                visited.add(m)
                visit_fn(m, n)
                queue.append(m)

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

    def visit_fn(n, parent):
        nonlocal oxygen
        intputer = intputers[parent].copy()
        dir = Direction(n - parent)
        input = dir_to_input[dir.str()]
        output = []
        intputer.run([input], output)
        status = output[0]
        if status == 0:
            walls.add(n)
        elif status == 1:
            pass
        elif status == 2:
            oxygen = n
        else:
            raise Exception(f'unknown status {status}')

        if status != 0:
            intputers[n] = intputer
            origin_distances[n] = origin_distances[parent] + 1

    def get_neighbor_fn(n):
        if n in walls:
            return []
        possible_neighbors = [n + d.vec() for d in all_directions]
        return [m for m in possible_neighbors if (m not in walls)]

    do_bfs(origin, get_neighbor_fn, visit_fn)

    show_map()

    if oxygen is None:
        raise Exception('oxygen not found')

    part1 = origin_distances[oxygen]

    oxygen_distances = {oxygen: 0}

    def visit_fn(n, parent):
        oxygen_distances[n] = oxygen_distances[parent] + 1

    do_bfs(oxygen, get_neighbor_fn, visit_fn)
    part2 = max(oxygen_distances.values())

    return part1, part2

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2: {part2}')
