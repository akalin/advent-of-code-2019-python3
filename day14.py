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

def reduce_chem(reactions, start, nstart, need=None):
    if not need:
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
    return need

def compute_day14(input):
    reactions = parse_reactions(input)
    need = reduce_chem(reactions, 'FUEL', 1)
    part1 = need['ORE']

    total_ore = 1000000000000
    fuel = 1
    while True:
        need = reduce_chem(reactions, 'FUEL', fuel)
        if need['ORE'] > total_ore:
            fuel //= 2
            break
        fuel *= 2

    print(fuel)

    while True:
        need = reduce_chem(reactions, 'FUEL', fuel)
        if need['ORE'] > total_ore:
            fuel -= 100
            break
        fuel += 100

    while True:
        need = reduce_chem(reactions, 'FUEL', fuel)
        if need['ORE'] > total_ore:
            fuel -= 1
            break
        fuel += 1

    return part1, fuel

if __name__ == '__main__':
    with open('day14.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day14(input)
        print(f'part 1: {p1}, part 2: {p2}')
