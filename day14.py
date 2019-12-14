from math import gcd
import collections
import itertools
from util import *
from vec2 import *
from vec3 import *

def parse_chem(s):
    q, chem = s.split(' ')
    return int(q), chem

def parse_reactions(input):
    reactions = {}
    lines = input.strip().split('\n')
    for line in lines:
        lhs, rhs = line.strip().split(' => ')
        m, chem = parse_chem(rhs)
        r_map = {}
        for dchem in lhs.split(', '):
            q, dchem = parse_chem(dchem)
            r_map[dchem] = q
        reactions[chem] = (m, r_map)
    return reactions

def reduce_chem(reactions, start, need=None):
    if not need:
        need = collections.defaultdict(int)
    need[start] = 1
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
    return need

def zero_point(need):
    for chem, n in need.items():
        if chem == 'ORE':
            continue
        if n != 0:
            return False
    return True

def compute_day14(input):
    reactions = parse_reactions(input)
    need = reduce_chem(reactions, 'FUEL')
    part1 = need['ORE']

    fuel = 0
    need = collections.defaultdict(int)
    while True:
        need = reduce_chem(reactions, 'FUEL', need)
        fuel += 1
        if zero_point(need):
            break
    x = need['ORE']
    total_ore = 1000000000000
    rat = total_ore // x
    total_fuel = rat * fuel
    rem_ore = total_ore - rat * x
    print('rem_ore', rem_ore)

    rem_fuel = 0
    need = None
    while True:
        next_need = reduce_chem(reactions, 'FUEL', need)
        print('what', next_need['ORE'])
        if next_need['ORE'] > rem_ore:
            break
        rem_fuel += 1
        need = next_need

    print('rem_fuel', rem_fuel)
    total_fuel += rem_fuel
    return part1, total_fuel

if __name__ == '__main__':
    with open('day14.input', 'r') as input_file:
        input = '''
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
'''
#        input = input_file.read()
        p1, p2 = compute_day14(input)
        print(f'part 1: {p1}, part 2: {p2}')
