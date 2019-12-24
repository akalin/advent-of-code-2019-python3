from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def new_level():
    rows = cols = 5
    new_level = [['.'] * cols for _ in range(rows)]
    new_level[2][2] = '?'
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
        for l, level in sorted(self.levels.items(),key=lambda x: x[0]):
            s += f'level {l}\n\n{self.to_string_level(level)}\n\n'
        return s

    def get_cell(self, x, y, l):
        level = self.get_level(l)
        rows = len(level)
        cols = len(level[0])
        if y < 0 or y >= rows:
            raise Exception('f {x} {y} {l}')
        if x < 0 or x >= cols:
            raise Exception('f {x} {y} {l}')
        if x == 2 and y == 2:
            raise Exception('f {x} {y} {l}')
        return level[y][x]

    def get_neighbors_from(self, x, y, l, dir):
        v = Vec2(x, y)
        x2, y2 = v + dir.vec()
        if x2 == 2 and y2 == 2:
            l2 = l+1
            idir = dir.turn_right().turn_right()
            c = Vec2(2, 2)
            m = c + idir.vec() + idir.vec()
            ldir = idir.turn_left()
            rdir = idir.turn_right()
            lef1 = m + ldir.vec()
            lef2 = lef1 + ldir.vec()
            r1 = m + rdir.vec()
            r2 = r1 + rdir.vec()
            for x3, y3 in [m, lef1, lef2, r1, r2]:
                yield (x3, y3, l2)
        elif x2 == -1:
            l2 = l-1
            yield (1, 2, l2)
        elif x2 == 5:
            l2 = l-1
            yield (3, 2, l2)
        elif y2 == -1:
            l2 = l-1
            yield (2, 1, l2)
        elif y2 == 5:
            l2 = l-1
            yield (2, 3, l2)
        else:
            yield x2, y2, l

    def get_neighbors(self, x, y, l):
        v = Vec2(x, y)
        for dir in all_directions:
            yield from self.get_neighbors_from(x, y, l, dir)

    def get_neighbor_bug_count(self, x, y, l):
        v = Vec2(x, y)
        bug_count = 0
        for x2, y2, l2 in self.get_neighbors(x, y, l):
#            print(f'gnbc: {x},{y},{l} {x2},{y2},{l2}')
            c = self.get_cell(x2, y2, l2)
            if c == '#':
                bug_count += 1
#        print(f'gnbc: {x},{y},{l} {list(self.get_neighbors(x, y, l))} {bug_count}')
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
        has_bug = False
        for y in range(rows):
            for x in range(cols):
                if x == 2 and y == 2:
                    continue
                new_lev[y][x] = self.next_cell(x, y, l)
                if new_lev[y][x] == '#':
                    has_bug = True
        return new_lev, has_bug

    def next_tick(self):
        g = Grid('')
        g.levels = {}
        for l, level in self.levels.items():
            g.levels[l] = self.next_level(l)[0]
        min_l, max_l = self.level_bounds()
        one_below, below_has_bug = self.next_level(min_l-1)
        one_above, above_has_bug = self.next_level(max_l+1)
        if below_has_bug:
            g.levels[min_l-1] = one_below
        if above_has_bug:
            g.levels[max_l+1] = one_above
        return g

    def level_bounds(self):
        min_level = min(self.levels.keys())
        max_level = max(self.levels.keys())
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

    def compute_bug_count(self):
        bug_count = 0
        rows = cols = 5
        for l, level in self.levels.items():
            for y in range(rows):
                for x in range(cols):
                    if x == 2 and y == 2:
                        continue
                    c = self.get_cell(x, y, l)
                    if c == '#':
                        bug_count += 1
        return bug_count

def compute_day24(input):
    input2 = '''
....#
#..#.
#.?##
..#..
#....
'''
    grid = Grid(input)

    for i in range(200):
#        print(f'i={i}')
#        print(grid.to_string())
#        print('')
        grid = grid.next_tick()

    print(grid.to_string())
    print(grid.compute_bug_count())

    return None, None

if __name__ == '__main__':
    with open('day24.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day24(input)
        print(f'part1: {part1}, part2: {part2}')
