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
            queue.extend([m])
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

def find_path_to_origin(n, parents):
    m = n
    path = []
    while m:
        path.append(m)
        m = parents[m]
    return path

def find_path(start, end, visited):
    start_to_x = find_path_to_origin(start, visited)
    end_to_x = find_path_to_origin(end, visited)
    while len(start_to_x) > 1 and len(end_to_x) > 1 and start_to_x[-1] == end_to_x[-1] and start_to_x[-2] == end_to_x[-2]:
        start_to_x.pop()
        end_to_x.pop()
    x_to_end = list(reversed(end_to_x))
    return start_to_x + x_to_end[1:]

def run_robot(program):
    intputer = Intputer(program)

    walls = set()
    oxygen = None

    pos = Vec2(0, 0)

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
        canvas.put_set(walls, '@')
        canvas.put((0, 0), 'o')
        canvas.put(pos, '*')
        if oxygen:
            canvas.put(oxygen, 'O')
        print(canvas.render(flip_y=True))

    def visit_fn(n, parent, visited):
        nonlocal pos
        nonlocal oxygen
        pos_to_parent = find_path(pos, parent, visited)
        for m in pos_to_parent[1:]:
            status = move_to(m)
            if status != 1 and status != 2:
                raise Exception(f'unexpected status {status}')
        move_to(n)

        return parent, True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    parents = do_dfs(pos, None, get_neighbor_fn, visit_fn)

    show_map()

    if oxygen is None:
        raise Exception('oxygen not found')

    shortest_path = find_path_to_origin(oxygen, parents)
    part1 = len(shortest_path) - 1

    def visit_fn(n, parent, visited):
        return visited[parent] + 1, True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls)

    counts = do_dfs(oxygen, 0, get_neighbor_fn, visit_fn)
    part2 = max(counts.values())

    return part1, part2

def compute_day15(input):
    program = parse_intcode(input)
    return run_robot(program)

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2: {part2}')
