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

def do_bfs(start, start_val, get_neighbor_fn, visit_fn):
    visited = {start: start_val}
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for m in get_neighbor_fn(n):
            if m in visited:
                continue
            val, should_continue = visit_fn(m, n, visited)
            visited[m] = val
            queue.append(m)
            if not should_continue:
                return visited
    return visited

def do_dfs(start, start_val, get_neighbor_fn, visit_fn):
    visited = {start: start_val}
    stack = [start]
    while stack:
        n = stack.pop()
        for m in get_neighbor_fn(n):
            if m in visited:
                continue
            val, should_continue = visit_fn(m, n, visited)
            visited[m] = val
            stack.append(m)
            if not should_continue:
                return visited
    return visited

def compute_day15(input):
    program = parse_intcode(input)
    intputer = Intputer(program)

    walls = set()
    oxygen = None
    origin = Vec2(0, 0)

    pos = origin

    dir_to_input = {
        'U': 1,
        'R': 4,
        'D': 2,
        'L': 3,
    }

    def move_to(neighbor):
        nonlocal pos
        nonlocal oxygen
        dir = Direction(neighbor - pos)
        input = dir_to_input[dir.str()]
        output = []
        intputer.run([input], output)
        status = output[0]
        if status == 0:
            walls.add(neighbor)
        elif status == 1:
            pos = neighbor
        elif status == 2:
            pos = neighbor
            oxygen = pos
        else:
            raise Exception(f'unknown status {status}')
        return status

    def show_map():
        canvas = ASCIICanvas()
        canvas.put_set(walls, '.')
        canvas.put(origin, 'o')
        canvas.put(pos, '*')
        if oxygen:
            canvas.put(oxygen, 'O')
        cls()
        print(canvas.render(flip_y=True))

    intputers = {}

    def visit_fn(n, parent, visited):
        nonlocal pos
        nonlocal oxygen
        nonlocal intputer
        if parent == pos:
            pass
        elif has_direction(parent - pos):
            move_to(parent)
        else:
            intputer = visited[parent][1].copy()
            pos = parent
        move_to(n)

        return (parent, intputer.copy()), True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    visited = do_dfs(origin, (None, intputer.copy()), get_neighbor_fn, visit_fn)

    show_map()

    if oxygen is None:
        raise Exception('oxygen not found')

    def visit_fn(n, parent, visited):
        return visited[parent] + 1, True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    counts = do_bfs(origin, 0, get_neighbor_fn, visit_fn)
    part1 = counts[oxygen]

    counts = do_bfs(oxygen, 0, get_neighbor_fn, visit_fn)
    part2 = max(counts.values())

    return part1, part2

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2: {part2}')
