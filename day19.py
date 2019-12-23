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
    output = run_single_program(program, [x, y])
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

def compute_day19(input):
    program = parse_intcode(input)
    num_tractor = 0
    k = 10000
    bounds = {}
    st4, end4 = find_tractor_bounds(program, 4, 0)
    bounds[4] = (st4, end4)
    sz = 100
    for y in range(5, k):
        hint = bounds[y-1][0]
        st, end = find_tractor_bounds(program, y, hint)
        print(y, st, end, end - st)
        bounds[y] = (st, end)
        if end - st >= sz and y >= sz - 1:
            prev_y = y - sz + 1
            if prev_y in bounds:
                print(f'checking prev_y {prev_y}')
                prev_st, prev_end = bounds[prev_y]
                st_fits = st >= prev_st and st < prev_end
                st_p100_fits = st+sz-1 >= prev_st and st+sz-1 < prev_end
                print('whaaat', y, st_fits, st_p100_fits)
                if st_fits and st_p100_fits:
                    print('found!', st, prev_y, st * 10000 + prev_y)
                    break

    return num_tractor, None

if __name__ == '__main__':
    with open('day19.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day19(input)
        print(f'part1: {part1}, part2: {part2}')
