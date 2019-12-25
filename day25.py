from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def compute_day25(input):
    program = parse_intcode(input)
    intputer = Intputer(program)

    commands_south = '''
south
east
donttake boulder
west
north
'''

    commands_east = '''
east
north
west
north
donttake whirled peas
west
west
take astronaut ice cream
south
south
'''

    commands_west = '''
west
take hypercube
south
north
west
west
west
east
north
take shell
west
donttake mug
south
take festive hat
north
east
south
west
east
east
east
east
'''

    commands = commands_south + commands_west + commands_east
    input = ascii_to_ints(commands)
    output = intputer.run_print(input)
    print(ints_to_ascii(output)[0])
    return None, None

if __name__ == '__main__':
    with open('day25.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day25(input)
        print(f'part1: {part1}, part2: {part2}')
