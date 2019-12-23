import collections
import itertools
from intcode import *
from util import *
from vec2 import *

def run_robot(program, initial_color):
    intputer = Intputer(program)
    grid = collections.defaultdict(int)
    pos = Vec2(0, 0)
    grid[pos] = initial_color
    dir = Direction('U')
    while True:
        input = [grid[pos]]
        output = intputer.run_simple([grid[pos]])
        if intputer.halted:
            break
        color, turn = output
        grid[pos] = color
        if turn == 0:
            dir = dir.turn_left()
        elif turn == 1:
            dir = dir.turn_right()
        else:
            raise Exception(f'unknown turn {turn}')
        pos += dir.vec()
    return grid

def compute_day11(input):
    program = parse_intcode(input)
    grid1 = run_robot(program, 0)
    grid2 = run_robot(program, 1)
    c_map = {
        0: ' ',
        1: '.',
    }
    canvas = ASCIICanvas()
    canvas.put_dict(grid2, c_map)
    return len(grid1), canvas.render(flip_y=True)

if __name__ == '__main__':
    with open('day11.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day11(input)
        print(f'part1: {part1}, part2:\n{part2}')
