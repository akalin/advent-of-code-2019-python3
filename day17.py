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
    sum = 0
    for x in range(1, rows - 2):
        for y in range(1, cols - 2):
            ch = lines[x][y]
            ch_l = lines[x-1][y]
            ch_r = lines[x+1][y]
            ch_u = lines[x][y+1]
            ch_d = lines[x][y-1]
            if ch + ch_u + ch_d + ch_l + ch_r == '#####':
                sum += x * y
    return sum, None

if __name__ == '__main__':
    with open('day17.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day17(input)
        print(f'part1: {part1}, part2: {part2}')
