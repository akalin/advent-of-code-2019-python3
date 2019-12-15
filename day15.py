from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *

dir_to_input = {
    'U': 1,
    'R': 4,
    'D': 2,
    'L': 3,
}

vec_to_dir = {
    Vec2(0, 1): 'U',
    Vec2(0, -1): 'D',
    Vec2(-1, 0): 'L',
    Vec2(1, 0): 'R',
}

def get_possible_neighbors(p):
    up = Direction('U')
    down = Direction('D')
    left = Direction('L')
    right = Direction('R')
    dirs = [up, down, left, right]
    possible_neighbors = [p + dir.vec() for dir in dirs]
    return possible_neighbors

def get_neighbors(p, walls, visited):
    if p in walls:
        return []
    possible_neighbors = get_possible_neighbors(p)
    neighbors = [n for n in possible_neighbors if (n not in walls) and (n not in visited)]
    return neighbors

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

def find_shortest_path(walls, start, end):
    def visit_fn(n, parent, _):
        return parent, n != end

    def get_neighbor_fn(n):
        return get_neighbors(n, walls, set())

    parents = do_bfs(start, None, get_neighbor_fn, visit_fn)

    n = end
    path = deque([end])
    while True:
        n = parents[n]
        if not n:
            break
        path.appendleft(n)
    return path

def find_next_dest(walls, visited, pos):
    candidates = visited
    candidates.add(pos)
    for c in candidates:
        neighbors = get_neighbors(c, walls, visited)
        for n in neighbors:
            return n

def find_path_to_origin(n, visited):
    m = n
    path = []
    while m:
        path.append(m)
        m = visited[m]
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

    def visit_fn(n, parent, visited):
        nonlocal pos
        nonlocal oxygen
        pos_to_parent = find_path(pos, parent, visited)
        print('path', pos, parent, pos_to_parent, n)
        for m in pos_to_parent[1:]:
            diff = m - pos
            dir = Direction(vec_to_dir[diff])
#            print(f'{pos} to {m} in dir {dir}')
            input = dir_to_input[dir.str()]
            output = []
            intputer.run([input], output)
            status = output[0]
            if status != 1 and status != 2:
                raise Exception(f'unexpected status {status}')
            pos = m

        diff = n - pos
        dir = Direction(vec_to_dir[diff])
        input = dir_to_input[dir.str()]
        output = []
        intputer.run([input], output)
        status = output[0]
        if status == 0:
            walls.add(n)
            path = []
        elif status == 1:
            pos = n
        elif status == 2:
            pos = n
            oxygen = pos
        else:
            raise Exception(f'unknown status {status}')

        print(f'status of {n} is {status}')

        canvas = ASCIICanvas()
#        canvas.put_set(visited, '.')
        canvas.put_set(walls, '@')
        canvas.put((0, 0), 'o')
        canvas.put(pos, '*')
        if oxygen:
            canvas.put(oxygen, 'O')
        print(canvas.render(flip_y=True))

        return parent, True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls, set())

    parents = do_dfs(pos, None, get_neighbor_fn, visit_fn)

    if oxygen is None:
        raise Exception('oxygen not found')

    shortest_path = find_shortest_path(walls, Vec2(0, 0), oxygen)
    print(f'shortest path {len(shortest_path) - 1}')
    part1 = len(shortest_path) - 1

    def visit_fn(n, parent, visited):
        return visited[parent] + 1, True

    def get_neighbor_fn(n):
        return get_neighbors(n, walls, set())

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
