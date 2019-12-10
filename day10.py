from math import gcd, atan2, pi

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

def compute_best_location(map):
    rows = map.strip().split('\n')
    grid = [list(row.strip()) for row in rows]
    asteroids = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.add((x, y))

    detected_counts = {a: count_detectable(a, asteroids) for a in asteroids}

    return max(detected_counts.items(), key=lambda i: i[1])

def find_next_asteroid(grid, asteroids, x, y, angle):
    mangle = -pi
    next_a = None
    for a in asteroids:
        if a == (x, y):
            continue
        x2, y2 = a
        if not can_detect(grid, x, y, x2, y2):
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
    input = '''
.#..#
.....
#####
....#
...##
'''
    input ='''
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
'''
    input='''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''
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

    input2 ='''
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
'''
    rows = input.strip().split('\n')
    grid = [list(row.strip()) for row in rows]
#    print(grid)
    rows = len(grid)
    cols = len(grid[0])
    asteroids = []
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '#':
                asteroids.append((x, y))

    visibles = [count_detectable(a, asteroids, grid) for a in asteroids]

#    for i, a in enumerate(asteroids):
#        print('vis', i, a, visibles[i])

    max_vis = max(range(len(visibles)), key=lambda i: visibles[i])
    mx, my = asteroids[max_vis]

    n = 1
    angle = pi + 0.0001
#    mx, my = (3, 8)
    while len(asteroids) > 1:
        na = find_next_asteroid(grid, asteroids, mx, my, angle)
        if not na:
            angle = pi + 0.0001
            continue
        x, y, nangle = na
        print(f'{n}: ({y}, {x}) a={nangle*180/pi}, {100*y+x}')
        grid[x][y] = '.'
        asteroids.remove((x, y))
        angle = nangle
        n += 1

    return (my, mx, visibles[max_vis]), None

if __name__ == '__main__':
    with open('day10.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day10(input)
        print(f'part : {p1}, part 2: {p2}')
