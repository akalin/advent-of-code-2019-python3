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
    output = run_intcode_program(program)
    img, nonascii = ints_to_ascii(output)
    if nonascii:
        raise nonascii
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
        next = pos + dir.vec(flip_y=True)
        if cell_eq(next, '#'):
            pos = next
            cur_leg += 1
        else:
            left_dir = dir.turn_left()
            right_dir = dir.turn_right()

            l_next = pos + left_dir.vec(flip_y=True)
            r_next = pos + right_dir.vec(flip_y=True)

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

    A = [
        ('R', 10),
        ('L', 8),
        ('R', 10),
        ('R', 4),
    ]
    B = [
        ('L', 6),
        ('L', 6),
        ('R', 10),
    ]

    C = [
        ('L', 6),
        ('R', 12),
        ('R', 12),
        ('R', 10),
    ]

    pairs2 = A + B + A + C + B + C + A + B + A + C

    if pairs != pairs2:
        raise

    main = 'A,B,A,C,B,C,A,B,A,C'

    def to_str(pairs):
        return ','.join([f'{t},{c}' for t, c in pairs])

    cmps = [main, to_str(A), to_str(B), to_str(C)]

    for x in [A, B, C]:
        print(len(to_str(x)))

    prog = '\n'.join(cmps) + '\nn\n'

    ss = ascii_to_ints(prog)

    print(program[0])
    program[0] = 2
    intputer = Intputer(program)

    (part2,) = intputer.run_print_ascii(iter(ss))
    return part1, part2

if __name__ == '__main__':
    with open('day17.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day17(input)
        print(f'part1: {part1}, part2: {part2}')
