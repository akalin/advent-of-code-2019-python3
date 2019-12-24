from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def get_cell(grid, x, y):
    rows = len(grid)
    cols = len(grid[0])
    if y < 0 or y >= rows:
        return None
    if x < 0 or x >= cols:
        return None
    return grid[y][x]

def get_neighbor_bug_count(grid, x, y):
    v = Vec2(x, y)
    bug_count = 0
    for dir in all_directions:
        x2, y2 = v + dir.vec()
        c = get_cell(grid, x2, y2)
        if c == '#':
            bug_count += 1
    return bug_count

def next_cell(grid, x, y):
    c = get_cell(grid, x, y)
    bug_count = get_neighbor_bug_count(grid, x, y)
    if c == '#':
        if bug_count == 1:
            return '#'
        return '.'
    else:
        if bug_count == 1 or bug_count == 2:
            return '#'
        return '.'

def next_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [['.'] * cols for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            new_grid[y][x] = next_cell(grid, x, y)
    return new_grid

def compute_biodiversity(grid):
    score = 0
    rows = len(grid)
    cols = len(grid[0])
    i = 0
    for y in range(rows):
        for x in range(cols):
            if get_cell(grid, x, y) == '#':
                print(score, i)
                score += (1 << i)
            i += 1
    return score

def grid_to_string(grid):
    return '\n'.join([''.join(line) for line in grid])

def compute_day24(input):
    grid = [[x for x in line.strip()] for line in input.strip().split('\n')]
    print(input, grid)

    grids = {}
    
    for i in range(1000):
        grids[grid_to_string(grid)] = i
        print(f'i={i}')
        print(grid_to_string(grid))
        print('')
        grid = next_grid(grid)
        if grid_to_string(grid) in grids:
            print('repeated', grids[grid_to_string(grid)])
            print(grid_to_string(grid))
            print(compute_biodiversity(grid))
            break

    return None, None

if __name__ == '__main__':
    with open('day24.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day24(input)
        print(f'part1: {part1}, part2: {part2}')
