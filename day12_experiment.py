from math import gcd

def do_single_step(ps, vs):
    n = len(ps)
    acs = [0] * n
    for i, p1 in enumerate(ps):
        for k, p2 in enumerate(ps[i+1:]):
            if p1 < p2:
                acs[i] += 1
                acs[i+k+1] -= 1
            elif p1 > p2:
                acs[i] -= 1
                acs[i+k+1] += 1

    vs_new = [vs[i] + acs[i] for i in range(n)]
    ps_new = [ps[i] + vs_new[i] for i in range(n)]
    return ps_new, vs_new, acs

def compute_period(ps0, vs0):
    n_steps = 0
    ps, vs = ps0, vs0
    print(ps, vs)
    while True:
        ps, vs, acs = do_single_step(ps, vs)
        print(ps, vs, acs)
        n_steps += 1
        if (ps, vs) == (ps0, vs0):
            return n_steps

if __name__ == '__main__':
    ps0 = [4, 13, 17, 16]
    vs0 = [0, 0, 0, 0]
    print(compute_period(ps0, vs0))
