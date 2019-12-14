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

def compute_ore_req(reactions, start, nstart):
    need = collections.defaultdict(int)
    need[start] = nstart
    while True:
        need_chems = [chem for chem, q in need.items() if chem != 'ORE' and q > 0]
        if len(need_chems) == 0:
            break

        chem = need_chems[0]
        q = need[chem]
#        print(f'need {q} of {chem}')
        (m, r_map) = reactions[chem]
        ratio = (q + (m - 1)) // m
#        print(f'can produce {m} of {chem}, so running reaction {ratio} times')
        for dchem, r in r_map.items():
#            print(f'  need {r * ratio} more of {dchem}')
            need[dchem] += r * ratio
#        print(f'now need {q - m*ratio} of {chem}')
        need[chem] = q - m*ratio
#        print(need)
    return need['ORE']

def compute_day14(input):
    reactions = parse_reactions(input)
    part1 = compute_ore_req(reactions, 'FUEL', 1)

    total_ore = 1000000000000
    fuel = 1
    while True:
        ore_req = compute_ore_req(reactions, 'FUEL', fuel)
        if ore_req > total_ore:
            fuel //= 2
            break
        fuel *= 2

    print(fuel)

    while True:
        ore_req = compute_ore_req(reactions, 'FUEL', fuel)
        if ore_req > total_ore:
            fuel -= 100
            break
        fuel += 100

    while True:
        ore_req = compute_ore_req(reactions, 'FUEL', fuel)
        if ore_req > total_ore:
            fuel -= 1
            break
        fuel += 1

    return part1, fuel

if __name__ == '__main__':
    with open('day14.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day14(input)
        print(f'part 1: {p1}, part 2: {p2}')
