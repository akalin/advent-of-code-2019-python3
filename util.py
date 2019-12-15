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
