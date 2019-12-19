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

def compute_day19(input):
    program = parse_intcode(input)
    num_tractor = 0
    for x in range(50):
        for y in range(50):
            if is_tractor(program, x, y):
                num_tractor += 1
    return num_tractor, None

if __name__ == '__main__':
    with open('day19.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day19(input)
        print(f'part1: {part1}, part2: {part2}')
