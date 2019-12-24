from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def new_level():
    rows = cols = 5
    new_level = [['.'] * cols for _ in range(rows)]
    return new_level

class Grid(object):
    def __init__(self, input):
        self.levels = {}
        self.levels[0] = [[x for x in line.strip()] for line in input.strip().split('\n')]

    def get_level(self, level):
        if level in self.levels:
            return self.levels[level]
        return new_level()

    def to_string_level(self, level):
        return '\n'.join([''.join(line) for line in level])

    def to_string(self):
        s = ''
        for l, level in self.levels.items():
            s += f'level {l}\n\n{self.to_string_level(level)}'
        return s

    def get_cell(self, x, y, l):
        level = self.get_level(l)
        rows = len(level)
        cols = len(level[0])
        if y < 0 or y >= rows:
            return None
        if x < 0 or x >= cols:
            return None
        return level[y][x]

    def get_neighbor_bug_count(self, x, y, l):
        v = Vec2(x, y)
        bug_count = 0
        for dir in all_directions:
            x2, y2 = v + dir.vec()
            c = self.get_cell(x2, y2, l)
            if c == '#':
                bug_count += 1
        return bug_count

    def next_cell(self, x, y, l):
        c = self.get_cell(x, y, l)
        bug_count = self.get_neighbor_bug_count(x, y, l)
        if c == '#':
            if bug_count == 1:
                return '#'
            return '.'
        else:
            if bug_count == 1 or bug_count == 2:
                return '#'
            return '.'

    def next_level(self, l):
        level = self.get_level(l)
        rows = len(level)
        cols = len(level[0])
        new_lev = new_level()
        for y in range(rows):
            for x in range(cols):
                new_lev[y][x] = self.next_cell(x, y, l)
        return new_lev

    def next_tick(self):
        g = Grid('')
        g.levels = {}
        for l, level in self.levels.items():
            g.levels[l] = self.next_level(l)
        min_l, max_l = self.level_bounds()
        one_below = self.next_level(min_l-1)
        one_above = self.next_level(max_l-1)
        if self.to_string_level(one_below) != self.to_string_level(new_level()):
            g.levels[min_l-1] = one_below
        if self.to_string_level(one_above) != self.to_string_level(new_level()):
            g.levels[max_l-1] = one_above
        return g

    def level_bounds(self):
        min_level = min(self.levels.keys())
        max_level = min(self.levels.keys())
        return min_level, max_level

    def compute_biodiversity(self, l):
        score = 0
        level = self.get_level(l)
        rows = len(level)
        cols = len(level[0])
        i = 0
        for y in range(rows):
            for x in range(cols):
                if self.get_cell(x, y, l) == '#':
                    print(score, i)
                    score += (1 << i)
            i += 1
        return score

def compute_day24(input):
    grid = Grid(input)

    for i in range(10):
        print(f'i={i}')
        print(grid.to_string())
        grid = grid.next_tick()
        print('')

    return None, None

if __name__ == '__main__':
    with open('day24.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day24(input)
        print(f'part1: {part1}, part2: {part2}')
