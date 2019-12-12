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
    k = 0
    pz0 = ith_slice(ps, i)
    vz0 = ith_slice(vs, i)

    seen = {}
    pz = copy_slice(pz0)
    vz = copy_slice(vz0)
    n_steps = 0
    seen[str((pz, vz))] = 0
    while True:
        do_single_step(pz, vz)
        n_steps += 1
        s = str((pz, vz))
        if s in seen:
            return seen[s], n_steps
        seen[s] = n_steps

def gcd_n(l):
    g = l[0]
    for n in l:
        g = gcd(g, n)
    return g

def prod_n(l):
    p = 1
    for n in l:
        p *= n
    return p

def lcm_n(l):
    return prod_n(l) // gcd_n(l)

def compute_day12(input):
    lines = [line.strip() for line in input.strip().split('\n')]
    ps0 = [parse_position(line) for line in lines]
    vs0 = [[0, 0, 0] for line in lines]

    n = len(ps0)
    m = len(ps0[0])

    periods = []
    for i in range(m):
        per = compute_ith_period(ps0, vs0, i)
        print(f'{i} period is {per}')
        periods.append(per)
    print(periods)
    print(gcd_n(periods))
    print(lcm_n(periods))
    return None, None

if __name__ == '__main__':
    with open('day12.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day12(input)
        print(f'part 1: {p1}, part 2: {p2}')
