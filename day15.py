from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *

def get_neighbors(p, walls):
    if p in walls:
        return []
    possible_neighbors = [p + d.vec() for d in all_directions]
    return [n for n in possible_neighbors if (n not in walls)]

def do_bfs(start, get_neighbor_fn, visit_fn):
    visited = set([start])
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for m in get_neighbor_fn(n):
            if m in visited:
                continue
            visit_fn(m, n)
            visited.add(m)
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

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    do_bfs(origin, get_neighbor_fn, visit_fn)

    show_map()

    if oxygen is None:
        raise Exception('oxygen not found')

    counts = {origin: 0}
    
    def visit_fn(n, parent):
        counts[n] = counts[parent] + 1

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    do_bfs(origin, get_neighbor_fn, visit_fn)
    part1 = counts[oxygen]

    counts = {oxygen: 0}
    do_bfs(oxygen, get_neighbor_fn, visit_fn)
    part2 = max(counts.values())

    return part1, part2

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2: {part2}')
