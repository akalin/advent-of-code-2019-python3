from math import gcd

def do_single_step(ps, vs):
    n = len(ps)
    m = len(ps[0])
    for i in range(n):
        p1 = ps[i]
        v1 = vs[i]
        for j in range(i+1, n):
            p2 = ps[j]
            v2 = vs[j]
            for k in range(m):
                if p1[k] < p2[k]:
                    v1[k] += 1
                    v2[k] -= 1
                elif p1[k] > p2[k]:
                    v1[k] -= 1
                    v2[k] += 1

    for i in range(n):
        p = ps[i]
        v = vs[i]
        for k in range(m):
            p[k] += v[k]

def parse_position(line):
    t = line.strip()[1:-1]
    vals = t.split(', ')
    return [int(val.split('=')[1]) for val in vals]

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
    s = []
    for p in ps:
        s.append([p[i]])
    return s

def copy_slice(sl):
    return [[s[0]] for s in sl]

def compute_ith_period(ps, vs, i):
    pz0 = ith_slice(ps, i)
    vz0 = ith_slice(vs, i)

    pz = ith_slice(ps, i)
    vz = ith_slice(vs, i)
    n_steps = 0
    while True:
        do_single_step(pz, vz)
        n_steps += 1
        if (pz, vz) == (pz0, vz0) and n_steps > 0:
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
    vs = [[0, 0, 0] for line in lines]
    for i in range(1000):
        do_single_step(ps, vs)

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
