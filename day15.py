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
    possible_neighbors = get_possible_neighbors(p)
    neighbors = [n for n in possible_neighbors if (n not in walls) and (n not in visited)]
    return neighbors

def find_shortest_path(walls, start, end):
    path_to = {}
    queue = deque([deque([start])])
    while queue:
        p = queue.popleft()
        p_end = p[-1]
        if p_end == end:
            return p
        path_to[p_end] = p
        neighbors = get_neighbors(p_end, walls, path_to)
        for n in neighbors:
            n_path = p.copy()
            n_path.extend([n])
            queue.extend([n_path])
    raise Exception('unexpected end')

def find_next_dest(walls, visited, pos):
    candidates = visited
    candidates.add(pos)
    for c in candidates:
        neighbors = get_neighbors(c, walls, visited)
        for n in neighbors:
            return n

def run_robot(program):
    intputer = Intputer(program)
    walls = set()
    visited = set()
    pos = Vec2(0, 0)
    visited.add(pos)
    dir = Direction('U')
    next_dest = find_next_dest(walls, visited, pos)
    path = find_shortest_path(walls, pos, next_dest)
    path.popleft()
    print('initial path', pos, path)
    while True:
        next_dest = path.popleft()
        diff = next_dest - pos
        dir = Direction(vec_to_dir[diff])
        input = dir_to_input[dir.str()]
#        print(f'{pos} {next_dest}, {path}, walls={walls}, visted={visited}')

        output = []
        intputer.run([input], output)
        status = output[0]
        if status == 0:
            walls.add(pos + dir.vec())
            path = []
        elif status == 1:
            print(f'pos was {pos} dir is {dir}')
            pos += dir.vec()
            print(f'adding {pos}')
            visited.add(pos)
        elif status == 2:
            break
        else:
            raise Exception(f'unknown status {status}')

        print(f'status={status}')

        canvas = ASCIICanvas()
        canvas.put_set(walls, 'X')
        canvas.put_set(visited, '.')
        canvas.put((0, 0), 'o')
        canvas.put(pos, '*')
        print(canvas.render(flip_y=True))

        if len(path) == 0:
            print('finding next dest')
            next_dest = find_next_dest(walls, visited, pos)
            print(f'finding shortest_path {pos} {next_dest}')
            path = find_shortest_path(walls, pos, next_dest)
            path.popleft()
            print('new path', pos, next_dest, path)

    return None

def compute_day15(input):
    program = parse_intcode(input)
    part1 = run_robot(program)
    return part1, None

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2:\n{part2}')
