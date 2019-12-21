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

def is_tractor(program, x, y):
    intputer = Intputer(program)
    output = []
    intputer.run([x, y], output)
    return output[0] == 1

def find_tractor_start(program, y, hint):
    x = hint
    while not is_tractor(program, x, y):
        x += 1
    return x

def find_tractor_bounds(program, y, hint):
    s = find_tractor_start(program, y, hint)

    ub = s + 1
    while is_tractor(program, ub, y):
        ub *= 2

    if ub == s:
        raise Exception('ub unexpectedly s')

    lb = s

    while ub > lb + 1:
        x = lb + (ub - lb) // 2
        if is_tractor(program, x, y):
            lb = x
        else:
            ub = x

    return (s, ub)

def fits(pts, x, y):
    return ((x, y) in pts) and ((x, y + 100) in pts) and ((x + 100, y) in pts) and ((x + 100, y + 100) in pts)

def compute_day21(input):
    program = parse_intcode(input)
    intputer = Intputer(program)
    input_s = '''NOT C J
AND D J
NOT A T
OR T J
WALK
'''
    input = [ord(x) for x in input_s]
    output = []
    intputer.run(input, output)
    print(output)
    output_s = ''.join([chr(x) for x in output])
    print(output_s)

    return None, None

if __name__ == '__main__':
    with open('day21.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day21(input)
        print(f'part1: {part1}, part2: {part2}')
