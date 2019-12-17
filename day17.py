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

def compute_day17(input):
    program = parse_intcode(input)
    intputer = Intputer(program)
    output = []
    intputer.run([], output)
    img = ''.join([chr(x) for x in output])
    lines = img.strip().split('\n')
    rows = len(lines)
    cols = len(lines[0])
    part1 = 0
    print(img)
    pos = None
    for y in range(1, rows - 2):
        for x in range(1, cols - 2):
            ch = lines[y][x]
            ch_l = lines[y-1][x]
            ch_r = lines[y+1][x]
            ch_u = lines[y][x+1]
            ch_d = lines[y][x-1]
            if ch + ch_u + ch_d + ch_l + ch_r == '#####':
                part1 += x * y
            if ch == '^':
                pos = Vec2(x, y)

    if not pos:
        raise

    def cell_eq(p, ch):
        x, y = p
        return y >= 0 and y < rows and x >= 0 and x < cols and lines[y][x] == ch

    dir = Direction('U')
    last_turn = None
    cur_leg = None
    pairs = []
    done = False
    while not done:
        next = pos + dir.vec()
        if cell_eq(next, '#'):
            pos = next
            cur_leg += 1
        else:
            left_dir = dir.turn_left()
            right_dir = dir.turn_right()

            l_next = pos + left_dir.vec()
            r_next = pos + right_dir.vec()

            if cell_eq(l_next, '#'):
                next_dir = left_dir
                turn = 'L'
            elif cell_eq(r_next, '#'):
                next_dir = right_dir
                turn = 'R'
            else:
                done = True

            if cur_leg is not None:
                pairs.append((last_turn, cur_leg))

            last_turn = turn
            dir = next_dir
            cur_leg = 0

    for p in pairs:
        print(p)

    return part1, None

if __name__ == '__main__':
    with open('day17.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day17(input)
        print(f'part1: {part1}, part2: {part2}')
