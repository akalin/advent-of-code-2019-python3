from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def is_close(c1, c2):
    return manhattan_norm([x1 - x2 for x1, x2 in zip(c1, c2)]) <= 3

def in_same_constellation(i, c, constellations):
    for c2, i2 in constellations.items():
        if i2 != i:
            continue
        if is_close(c, c2):
            return True
    return False

def parse_input(input):
    lines = input.strip().split('\n')
    return [tuple(int(x) for x in line.strip().split(',')) for line in lines]

def get_constellation_count(points):
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

    return len(set(constellations.values()))

def compute_day25(input):
    points = parse_input(input)
    part1 = get_constellation_count(points)

    return part1, None

if __name__ == '__main__':
    with open('day25_2018.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day25(input)
        print(f'part1: {part1}, part2: {part2}')
