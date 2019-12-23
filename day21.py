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
    output = run_intcode_program(program, [ord(x) for x in input_s])
    print(output[-1])
    output_s = ''.join([chr(x) for x in output])
    print(output_s)

    return None, None

if __name__ == '__main__':
    with open('day21.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day21(input)
        print(f'part1: {part1}, part2: {part2}')
