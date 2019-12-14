from math import gcd
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


def parse_position(line):
    t = line.strip()[1:-1]
    vals = t.split(', ')
    return Vec3([int(val.split('=')[1]) for val in vals])

def int_sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return +1
    return 0

def vec3_sgn(v):
    return Vec3([int_sgn(x) for x in v])

def do_single_step(ps, vs, zero, sgn_fn):
    n = len(ps)
    accs = [zero] * n

    for i in range(n):
        p1 = ps[i]
        for j in range(i+1, n):
            p2 = ps[j]
            sgn = sgn_fn(p2 - p1)
            accs[i] += sgn
            accs[j] -= sgn

    for i in range(n):
        vs[i] += accs[i]

    for i in range(n):
        ps[i] += vs[i]

def compute_energy(ps, vs):
    n = len(ps)
    m = len(ps[0])
    e = 0
    for i in range(n):
        pe = 0
        ke = 0
        p = ps[i]
        v = vs[i]
        for k in range(m):
            pe += abs(p[k])
            ke += abs(v[k])
        e += pe * ke
    return e

def ith_slice(ps, i):
    return [p[i] for p in ps]

def compute_ith_period(ps, vs, i):
    pz0 = ith_slice(ps, i)
    vz0 = ith_slice(vs, i)

    pz = pz0[:]
    vz = vz0[:]
    n_steps = 0
    while True:
        do_single_step(pz, vz, 0, int_sgn)
        n_steps += 1
        if (pz, vz) == (pz0, vz0):
            return n_steps

def lcm(x, y):
    return x * y // gcd(x, y)

def lcm_n(l):
    res = l[0]
    for n in l[1:]:
        res = lcm(res, n) 
    return res

def compute_day12(input):
    lines = [line.strip() for line in input.strip().split('\n')]
    ps = [parse_position(line) for line in lines]
    vs = [Vec3(0, 0, 0) for line in lines]
    for i in range(1000):
        do_single_step(ps, vs, Vec3(0, 0, 0), vec3_sgn)

    part1 = compute_energy(ps, vs)

    ps = [parse_position(line) for line in lines]
    vs = [[0, 0, 0] for line in lines]
    m = len(ps[0])
    periods = [compute_ith_period(ps, vs, i) for i in range(m)]
    part2 = lcm_n(periods)
    return part1, part2

if __name__ == '__main__':
    with open('day12.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day12(input)
        print(f'part 1: {p1}, part 2: {p2}')
