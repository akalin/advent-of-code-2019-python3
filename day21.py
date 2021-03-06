from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *

def compute_day21(input):
    program = parse_intcode(input)
# not b, not e or not g, d, h
# not b, not g, d, h
# not c, d, h
# not i, h, d
# not a
    input_s = '''NOT G J
NOT E T
OR J T
NOT B J
AND T J
AND D J
AND H J
NOT C T
AND D T
AND H T
OR T J
NOT A T
OR T J
RUN
'''
    intputer = Intputer(program)
    input = ascii_to_ints(input_s)
    (part2,) = intputer.run_print(input, print_input=False, print_non_ascii=False, print_output=False)

    return None, part2

if __name__ == '__main__':
    with open('day21.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day21(input)
        print(f'part1: {part1}, part2: {part2}')
