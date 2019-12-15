from vec2 import *

def manhattan_norm(v):
    return sum([abs(x) for x in v])

_dir_to_vec = {
    'U': Vec2(0, 1),
    'D': Vec2(0, -1),
    'L': Vec2(-1, 0),
    'R': Vec2(1, 0),
}

_dir_to_left = {
    'U': 'L',
    'L': 'D',
    'D': 'R',
    'R': 'U',
}

_dir_to_right = {
    'U': 'R',
    'R': 'D',
    'D': 'L',
    'L': 'U',
}

class Direction(object):
    def __init__(self, direction):
        _dir_to_vec[direction]
        self._dir = direction

    def vec(self):
        return _dir_to_vec[self._dir]

    def turn_left(self):
        return self.__class__(_dir_to_left[self._dir])

    def turn_right(self):
        return self.__class__(_dir_to_right[self._dir])

    def __repr__(self):
        return f'Direction{{self._dir}}'

class ASCIICanvas(object):
    def __init__(self, default_c = ' '):
        self._default_c = default_c
        self._pixels = {}

    def draw_pixel(self, x, y, c):
        self._pixels[(x, y)] = c

    def render(self, flip_y=False):
        min_x = min([x for x, y in self._pixels.keys()])
        max_x = max([x for x, y in self._pixels.keys()])
        min_y = min([y for x, y in self._pixels.keys()])
        max_y = max([y for x, y in self._pixels.keys()])
        grid = []
        for i in range(max_y - min_y + 1):
            grid.append([self._default_c] * (max_x - min_x + 1))
        for (x, y), c in self._pixels.items():
            grid[y - min_y][x - min_x] = c
        rows = [''.join(row) for row in grid]
        if flip_y:
            rows = reversed(rows)
        return '\n'.join(rows)

    def __str__(self):
        return self.render()
