from math import gcd
import itertools
from util import *
from vec3 import *

def parse_position(line):
    t = line.strip()[1:-1]
    vals = t.split(', ')
    return Vec3([int(val.split('=')[1]) for val in vals])

def vec3_sgn(v):
    return Vec3([int_sgn(x) for x in v])

def do_single_step(ps, vs, zero, sgn_fn):
    n = len(ps)
    accs = [zero] * n
    for (i, p1), (j, p2) in itertools.combinations(enumerate(ps), 2):
        sgn = sgn_fn(p2 - p1)
        accs[i] += sgn
        accs[j] -= sgn

    next_vs = [v + a for v, a in zip(vs, accs)]
    next_ps = [p + v for p, v in zip(ps, next_vs)]
    return next_ps, next_vs

def compute_energy(ps, vs):
    return sum([manhattan_norm(p) * manhattan_norm(v) for p, v in zip(ps, vs)])

def compute_period(pz0, vz0):
    pz, vz = pz0, vz0
    n_steps = 0
    while True:
        pz, vz = do_single_step(pz, vz, 0, int_sgn)
        n_steps += 1
        if (pz, vz) == (pz0, vz0):
            return n_steps

def lcm(x, y):
    return x * y // gcd(x, y)

def lcm_n(l):
    res = 1
    for n in l:
        res = lcm(res, n) 
    return res

def compute_day12(input):
    lines = [line.strip() for line in input.strip().split('\n')]
    ps0 = [parse_position(line) for line in lines]
    vs0 = [Vec3(0, 0, 0) for line in lines]

    ps, vs = ps0, vs0
    for i in range(1000):
        ps, vs = do_single_step(ps, vs, Vec3(0, 0, 0), vec3_sgn)
    part1 = compute_energy(ps, vs)

    p_slices = [list(pz) for pz in zip(*ps)]
    v_slices = [list(vz) for vz in zip(*vs)]
    periods = [compute_period(pz, vz) for pz, vz in zip(p_slices, v_slices)]
    part2 = lcm_n(periods)
    return part1, part2

if __name__ == '__main__':
    with open('day12.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day12(input)
        print(f'part 1: {p1}, part 2: {p2}')
