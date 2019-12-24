from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def in_same_constellation(i, c, constellations):
    for c2, i2 in constellations.items():
        if i2 != i:
            continue
        if manhattan_norm([c[i] - c2[i] for i in range(len(c))]) <= 3:
            return True
    return False

def compute_day25(input):
    input = '''
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
'''
    lines = input.strip().split('\n')
    points = [tuple(int(x) for x in line.strip().split(',')) for line in lines]

    constellations = {p: i for i, p in enumerate(points)}

    while True:
        did_work = False
        for c1, i1 in constellations.items():
            for c2, i2 in constellations.items():
                if i1 == i2:
                    continue
                if in_same_constellation(i1, c2, constellations):
                    did_work = True
                    for c3, i3 in constellations.items():
                        if i3 == i2:
                            constellations[c3] = i1
        if not did_work:
            break

    part1 = len(set(constellations.values()))

    return part1, None

if __name__ == '__main__':
    with open('day25_2018.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day25(input)
        print(f'part1: {part1}, part2: {part2}')
