from math import gcd
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

def parse_asteroids(input):
    rows = input.strip().split('\n')
    return set(Vec2(x, y) for y, row in enumerate(rows) for x, cell in enumerate(row.strip()) if cell == '#')

def can_detect(asteroids, a1, a2):
    dx, dy = a2 - a1
    g = gcd(dx, dy)
    s = Vec2(dx // g, dy // g)

    v = a1 + s
    while v != a2:
        if v in asteroids:
            return False
        v += s

    return True

def count_detectable(a1, asteroids):
    return sum(1 for a2 in asteroids - set([a1]) if can_detect(asteroids, a1, a2))

def compute_best_location(asteroids):
    detected_counts = ((a, count_detectable(a, asteroids)) for a in asteroids)
    return max(detected_counts, key=lambda x: x[1])

def compute_angle(a1, a2):
    dx, dy = a2 - a1
    if dx == 0:
        if dy == 0:
            raise Exception(f'a1 == a2 == {a1}')
        if dy < 0:
            # North
            return (1, 0)
        # South
        return (3, 0)
    if dx > 0:
        # East
        return (2, dy/dx)
    # West
    return (4, dy/dx)

def vaporize_asteroids(asteroids, p):
    angles = [(a, compute_angle(p, a)) for a in asteroids - set([p])]
    sorted_angles = sorted(angles, key=lambda x: x[1])

    asteroids_left = asteroids.copy()
    while sorted_angles:
        next_round = []
        to_remove = []
        for a, angle in sorted_angles:
            if can_detect(asteroids_left, p, a):
                to_remove.append(a)
                yield a
            else:
                next_round.append((a, angle))
        if sorted_angles == next_round:
            raise Exception(f'sorted_angles stayed the same: {sorted_angles}')
        sorted_angles = next_round
        asteroids_left -= set(to_remove)

def compute_day10(input):
    asteroids = parse_asteroids(input)
    best, detected_count = compute_best_location(asteroids)

    gen = vaporize_asteroids(asteroids, best)
    for i in range(199):
        next(gen)
    x200, y200 = next(gen)
    return detected_count, x200*100+y200

if __name__ == '__main__':
    with open('day10.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day10(input)
        print(f'part 1: {p1}, part 2: {p2}')
