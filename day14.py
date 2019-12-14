import collections

def parse_chem(s):
    q, chem = s.split(' ')
    return int(q), chem

def parse_reactions(input):
    reactions = {}
    lines = input.strip().split('\n')
    for line in lines:
        lhs, rhs = line.strip().split(' => ')
        out_q, out_chem = parse_chem(rhs)
        inputs = {}
        for s in lhs.split(', '):
            in_q, in_chem = parse_chem(s)
            inputs[in_chem] = in_q
        reactions[out_chem] = (out_q, inputs)
    return reactions

def compute_ore_for_fuel(reactions, fuel_q):
    need = collections.defaultdict(int)
    need['FUEL'] = fuel_q
    while True:
        chem_q = next(((chem, q) for chem, q in need.items() if chem != 'ORE' and q > 0), None)
        if not chem_q:
            break
        chem, needed_q = chem_q

        (out_q, inputs) = reactions[chem]
        ratio = (needed_q + (out_q - 1)) // out_q
        need[chem] -= out_q * ratio
        for in_chem, in_q in inputs.items():
            need[in_chem] += in_q * ratio
    return need['ORE']

def compute_fuel_for_ore(reactions, ore_q):
    ub = 1
    while True:
        ore_for_fuel = compute_ore_for_fuel(reactions, ub)
        if ore_for_fuel > ore_q:
            break
        ub *= 2

    if ub == 1:
        raise Exception('ub unexpectedly 1')

    lb = ub // 2

    while ub > lb + 1:
        x = lb + (ub - lb) // 2
        ore_for_fuel = compute_ore_for_fuel(reactions, x)
        if ore_for_fuel > ore_q:
            ub = x
        else:
            lb = x

    return lb

def compute_day14(input):
    reactions = parse_reactions(input)
    part1 = compute_ore_for_fuel(reactions, 1)

    part2 = compute_fuel_for_ore(reactions, 1000000000000)
    return part1, part2

if __name__ == '__main__':
    with open('day14.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day14(input)
        print(f'part 1: {p1}, part 2: {p2}')
