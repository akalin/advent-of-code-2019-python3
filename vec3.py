import collections.abc

class Vec3(collections.abc.Sequence):
    def __init__(self, *args):
        if len(args) == 3:
            self._v = tuple(args)
        elif len(args) == 1 and len(args[0]) == 3:
            self._v = tuple(args[0])
        else:
            raise TypeError(f'Expected 3 arguments or a sequence of length 3, got {args}')

    def __len__(self):
        return len(self._v)

    def __getitem__(self, index):
        return self._v[index]

    def __str__(self):
        return f'Vec3{str(self._v)}'

    def __repr__(self):
        return f'Vec3{repr(self._v)}'

    def __hash__(self):
        return hash(self._v)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __eq__(self, other):
        ox, oy, oz = other
        return self.x == ox and self.y == oy and self.z == oz

    def __add__(self, other):
        ox, oy, oz = other
        return self.__class__(self.x + ox, self.y + oy, self.z + oz)

    def __sub__(self, other):
        ox, oy, oz = other
        return self.__class__(self.x - ox, self.y - oy, self.z - oz)
