import collections.abc

class Vec2(collections.abc.Sequence):
    def __init__(self, *args):
        if len(args) == 2:
            self._v = tuple(args)
        elif len(args) == 1 and len(args[0]) == 2:
            self._v = tuple(args[0])
        else:
            raise TypeError(f'Expected 2 arguments or a sequence of length 2, got {args}')

    def __len__(self):
        return len(self._v)

    def __getitem__(self, index):
        return self._v[index]

    def __str__(self):
        return f'Vec2{str(self._v)}'

    def __repr__(self):
        return f'Vec2{repr(self._v)}'

    def __hash__(self):
        return hash(self._v)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __eq__(self, other):
        ox, oy = other
        return self.x == ox and self.y == oy

    def __add__(self, other):
        ox, oy = other
        return self.__class__(self.x + ox, self.y + oy)

    def __sub__(self, other):
        ox, oy = other
        return self.__class__(self.x - ox, self.y - oy)
