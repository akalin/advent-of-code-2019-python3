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
    pred = {}
    queue = deque([start])
    pred[start] = None
    while queue:
        p = queue.popleft()
        if p == end:
            path = deque([end])
            while True:
                p = pred[p]
                if not p:
                    break
                path.appendleft(p)
            return path
        neighbors = get_neighbors(p, walls, pred)
        queue.extend(neighbors)
        for n in neighbors:
            pred[n] = p
    raise Exception('unexpected end')

def do_bfs(walls, start):
    counts = {}
    queue = deque([start])
    counts[start] = 0
    while queue:
        p = queue.popleft()
        neighbors = get_neighbors(p, walls, counts)
        queue.extend(neighbors)
        for n in neighbors:
            counts[n] = counts[p] + 1
    return max(counts.values())

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
    found = None
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
            pos += dir.vec()
            found = pos
            print(f'adding {pos} (found)')
            visited.add(pos)
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
            if next_dest is None:
                break
            print(f'finding shortest_path {pos} {next_dest}')
            path = find_shortest_path(walls, pos, next_dest)
            path.popleft()
            print('new path', pos, next_dest, path)

    shortest_path = find_shortest_path(walls, Vec2(0, 0), found)
    print(f'shortest path {len(shortest_path) - 1}')
    part1 = len(shortest_path) - 1

    part2 = do_bfs(walls, found) - 1

    return part1, part2

def compute_day15(input):
    program = parse_intcode(input)
    return run_robot(program)

if __name__ == '__main__':
    with open('day15.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day15(input)
        print(f'part1: {part1}, part2:\n{part2}')
