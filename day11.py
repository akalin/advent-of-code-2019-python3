import collections
import itertools
from intcode import *
from vec2 import *

def do_turn(dir, turn):
    if turn == 0:
        if dir == 'U':
            return 'L'
        if dir == 'L':
            return 'D'
        if dir == 'D':
            return 'R'
        if dir == 'R':
            return 'U'
    else:
        if dir == 'U':
            return 'R'
        if dir == 'R':
            return 'D'
        if dir == 'D':
            return 'L'
        if dir == 'L':
            return 'U'

def move_forward(pos, dir):
    if dir == 'U':
        return pos + (0, 1)
    if dir == 'D':
        return pos + (0, -1)
    if dir == 'L':
        return pos + (-1, 0)
    if dir == 'R':
        return pos + (1, 0)

def run_robot(program, initial_color):
    intputer = Intputer(program)
    grid = collections.defaultdict(int)
    pos = Vec2(0, 0)
    grid[pos] = initial_color
    dir = 'U'
    while True:
        input = [grid[pos]]
        output = []
        intputer.run(input, output)
        if intputer.halted:
            break
        color, turn = output
        grid[pos] = color
        dir = do_turn(dir, turn)
        pos = move_forward(pos, dir)
    return grid

def compute_day11(input):
    program = parse_intcode(input)
    grid1 = run_robot(program, 0)
    grid2 = run_robot(program, 1)
    min_x = min([x for x, y in grid2.keys()])
    max_x = max([x for x, y in grid2.keys()])
    min_y = min([y for x, y in grid2.keys()])
    max_y = max([y for x, y in grid2.keys()])
    grid3 = []
    for i in range(max_y - min_y + 1):
        grid3.append([' '] * (max_x - min_x + 1))
    for (x, y), c in grid2.items():
        if c == 0:
            grid3[y - min_y][x - min_x] = ' '
        elif c == 1:
            grid3[y - min_y][x - min_x] = '.'
        else:
            raise
    img = '\n'.join(reversed([''.join(row) for row in grid3]))
    return len(grid1), img

if __name__ == '__main__':
    with open('day11.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day11(input)
        print(f'part1: {part1}, part2:\n{part2}')
