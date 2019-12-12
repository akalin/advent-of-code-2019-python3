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

def compute_day12(input):
    lines = [line.strip() for line in input.strip().split('\n')]
    ps = [parse_position(line) for line in lines]
    vs = [[0, 0, 0] for line in lines]
    for i in range(1001):
        print(f'After {i} steps')
        for i in range(len(ps)):
            print(f'p={ps[i]} v={vs[i]}')
        print(f'e={compute_energy(ps, vs)}')
        do_single_step(ps, vs)
    return None, None

if __name__ == '__main__':
    with open('day12.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day12(input)
        print(f'part 1: {p1}, part 2: {p2}')
