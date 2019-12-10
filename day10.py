from math import gcd, atan2, pi

def parse_asteroids(input):
    rows = input.strip().split('\n')
    return set((x, y) for y, row in enumerate(rows) for x, cell in enumerate(row.strip()) if cell == '#')


def can_detect(asteroids, a1, a2):
    x1, y1 = a1
    x2, y2 = a2
    dx = x2 - x1
    dy = y2 - y1

    g = gcd(dx, dy)
    sx = dx // g
    sy = dy // g

    x = x1 + sx
    y = y1 + sy
    while (x, y) != (x2, y2):
        if (x, y) in asteroids:
            return False
        x += sx
        y += sy

    return True

def count_detectable(a1, asteroids):
    return sum(1 for a2 in asteroids - set([a1]) if can_detect(asteroids, a1, a2))

def compute_best_location(asteroids):
    detected_counts = ((a, count_detectable(a, asteroids)) for a in asteroids)
    return max(detected_counts, key=lambda i: i[1])

def find_next_asteroid(asteroids, p, angle):
    mangle = -pi
    next_a = None
    x, y = p
    for a in asteroids:
        if a == p:
            continue
        x2, y2 = a
        if not can_detect(asteroids, p, a):
            continue
        dx = x2 - x
        dy = y2 - y
        nangle = atan2(dy, dx)
        if nangle >= angle:
            continue
        if nangle > mangle:
            mangle = nangle
            next_a = a
    if next_a:
        x, y = next_a
        return x, y, mangle
    return None

def compute_day10(input):
    input='''
#....#.....#...#.#.....#.#..#....#
#..#..##...#......#.....#..###.#.#
#......#.#.#.....##....#.#.....#..
..#.#...#.......#.##..#...........
.##..#...##......##.#.#...........
.....#.#..##...#..##.....#...#.##.
....#.##.##.#....###.#........####
..#....#..####........##.........#
..#...#......#.#..#..#.#.##......#
.............#.#....##.......#...#
.#.#..##.#.#.#.#.......#.....#....
.....##.###..#.....#.#..###.....##
.....#...#.#.#......#.#....##.....
##.#.....#...#....#...#..#....#.#.
..#.............###.#.##....#.#...
..##.#.........#.##.####.........#
##.#...###....#..#...###..##..#..#
.........#.#.....#........#.......
#.......#..#.#.#..##.....#.#.....#
..#....#....#.#.##......#..#.###..
......##.##.##...#...##.#...###...
.#.....#...#........#....#.###....
.#.#.#..#............#..........#.
..##.....#....#....##..#.#.......#
..##.....#.#......................
.#..#...#....#.#.....#.........#..
........#.............#.#.........
#...#.#......#.##....#...#.#.#...#
.#.....#.#.....#.....#.#.##......#
..##....#.....#.....#....#.##..#..
#..###.#.#....#......#...#........
..#......#..#....##...#.#.#...#..#
.#.##.#.#.....#..#..#........##...
....#...##.##.##......#..#..##....
'''

    asteroids = parse_asteroids(input)
    best, detected_count = compute_best_location(asteroids)

    n = 1
    angle = pi + 0.0001
    while len(asteroids) > 1:
        na = find_next_asteroid(asteroids, best, angle)
        if not na:
            angle = pi + 0.0001
            continue
        x, y, nangle = na
        print(f'{n}: ({y}, {x}) a={nangle*180/pi}, {100*y+x}')
        asteroids.remove((x, y))
        angle = nangle
        n += 1

    return detected_count, None

if __name__ == '__main__':
    with open('day10.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day10(input)
        print(f'part 1: {p1}, part 2: {p2}')
