from math import gcd, atan2, pi

def rangeto(n):
    if n >= 0:
        return range(1, n)
    return range(-1, n, -1)

def rangeto2(n, dn):
    if n >= 0:
        return range(dn, n, dn)
    return range(dn, n, dn)

def is_visible(asteroids, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        for i in rangeto(dy):
            y3 = y1 + i
            if (x1, y3) in asteroids:
                return False
        return True

    if dy == 0:
        for i in rangeto(dx):
            x3 = x1 + i
            if (x3, y1) in asteroids:
                return False
        return True

    g = gcd(dx, dy)
    if g == 1:
        return True

    ddx = dx // g
    ddy = dy // g

#    print(f'is_visible p1=({x1}, {y1}), p2=({x2}, {y2}), d=({dx}, {dy}) g={g} dd=({ddx}, {ddy})')

    d3y = ddy
    for d3x in range(ddx, dx, ddx):
        x3 = x1 + d3x
        y3 = y1 + d3y
#        print(f'loop d3=({d3x}, {d3y}) p3=({x3}, {y3})')
        if (x3, y3) in asteroids:
#            print('found blocker')
            return False
        d3y += ddy

    return True

def count_visible(a1, asteroids):
    visible = 0
#    print('')
    for a2 in asteroids:
        if a1 == a2:
            continue
        x1, y1 = a1
        x2, y2 = a2
        v = is_visible(asteroids, x1, y1, x2, y2)
#        print('count', x1, y1, x2, y2, v)
        if v:
            visible += 1
#    print('vis', visible)
    return visible

def compute_best_asteroid(map):
    rows = map.strip().split('\n')
    grid = [list(row.strip()) for row in rows]
    asteroids = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.add((x, y))

    visibles = {a: count_visible(a, asteroids) for a in asteroids}

#    for i, a in enumerate(asteroids):
#        print('vis', i, a, visibles[i])

    return max(visibles.items(), key=lambda i: i[1])

def find_next_asteroid(grid, asteroids, x, y, angle):
    mangle = -pi
    next_a = None
    for a in asteroids:
        if a == (x, y):
            continue
        x2, y2 = a
        if not is_visible(grid, x, y, x2, y2):
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

    visibles = [count_visible(a, asteroids, grid) for a in asteroids]

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
