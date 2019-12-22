from vec2 import *
import os

def cls():
    os.system('clear')

def manhattan_norm(v):
    return sum([abs(x) for x in v])

def int_sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return +1
    return 0

_dir_to_vec = {
    'U': Vec2(0, +1),
    'D': Vec2(0, -1),
    'L': Vec2(-1, 0),
    'R': Vec2(1, 0),
}

_vec_to_dir = {v: d for d, v in _dir_to_vec.items()}

_dir_to_left = {
    'U': 'L',
    'L': 'D',
    'D': 'R',
    'R': 'U',
}

_dir_to_right = {v: d for d, v in _dir_to_left.items()}

def has_direction(v):
    return v in _vec_to_dir

class Direction(object):
    def __init__(self, arg):
        if arg in _dir_to_vec:
            self._dir = arg
        else:
            self._dir = _vec_to_dir[arg]

    def vec(self, flip_y=False):
        v = _dir_to_vec[self._dir]
        if flip_y:
            v = Vec2(v.x, -v.y)
        return v

    def turn_left(self):
        return self.__class__(_dir_to_left[self._dir])

    def turn_right(self):
        return self.__class__(_dir_to_right[self._dir])

    def str(self):
        return self._dir

    def __repr__(self):
        return f'Direction({self._dir})'

all_directions = [Direction(d) for d in _dir_to_vec.keys()]

class ASCIICanvas(object):
    def __init__(self, default_c = ' '):
        self._default_c = default_c
        self._pixels = {}

    def put(self, *args):
        if len(args) == 3:
            p = (args[0], args[1])
            c = args[2]
        elif len(args) == 2 and len(args[0]) == 2:
            p = (args[0][0], args[0][1])
            c = args[1]
        else:
            raise TypeError(f'Expected (x, y, c) or ((x, y), c), got {args}')
        self._pixels[p] = c

    def put_set(self, s, c):
        for p in s:
            self.put(p, c)

    def put_dict(self, d, c_map=None):
        for p, c in d.items():
            if c_map:
                self.put(p, c_map[c])
            else:
                self.put(p, c)

    def render(self, flip_y=False):
        if len(self._pixels) == 0:
            return ''

        it = iter(self._pixels.keys())
        first = next(it)
        min_x, min_y = first
        max_x, max_y = first
        for x, y in it:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
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

# from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def modinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g != 1:
        raise Exception(f'gcd(a, b) = {g} != 1')
    return x % b
