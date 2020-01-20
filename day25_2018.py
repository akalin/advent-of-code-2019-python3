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

def compute_day25(input):
    points = parse_input(input)
    part1 = get_constellation_count(points)

    return part1, None

if __name__ == '__main__':
    with open('day25_2018.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day25(input)
        print(f'part1: {part1}, part2: {part2}')
