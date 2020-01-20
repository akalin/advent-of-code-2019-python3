from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *
from util import *

def is_close(p1, p2):
    return manhattan_norm([x1 - x2 for x1, x2 in zip(p1, p2)]) <= 3

def is_same_constellation(c1, c2):
    return any([is_close(p1, p2) for p1 in c1 for p2 in c2])

def parse_input(input):
    lines = input.strip().split('\n')
    return [tuple(int(x) for x in line.strip().split(',')) for line in lines]

def get_constellation_count(points):
    constellations = [{p} for p in points]

    for i1, c1 in enumerate(constellations):
        if len(c1) == 0:
            continue
        while True:
            did_work = False
            for c2 in constellations[i1+1:]:
                if is_same_constellation(c1, c2):
                    did_work = True
                    c1 |= c2
                    c2.clear()
            if not did_work:
                break

    return len([c for c in constellations if len(c) > 0])

def compute_day01(input):
    lines = input.strip().split('\n')
    ints = [int(line.strip()) for line in lines]
    part1 = sum(ints)

    freq = 0
    frequencies = {0}
    found_freq = None
    while not found_freq:
        for i in ints:
            freq += i
            if freq in frequencies:
                found_freq = freq
                break
            frequencies.add(freq)
    return part1, found_freq

if __name__ == '__main__':
    with open('day01_2018.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day01(input)
        print(f'part1: {part1}, part2: {part2}')
