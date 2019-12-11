from math import gcd

def parse_asteroids(input):
    rows = input.strip().split('\n')
    return set((x, y) for y, row in enumerate(rows) for x, cell in enumerate(row.strip()) if cell == '#')

def vadd(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def vsub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def can_detect(asteroids, a1, a2):
    dx, dy = vsub(a2, a1)
    g = gcd(dx, dy)
    s = (dx // g, dy // g)

    v = vadd(a1, s)
    while v != a2:
        if v in asteroids:
            return False
        v = vadd(v, s)

    return True

def count_detectable(a1, asteroids):
    return sum(1 for a2 in asteroids - set([a1]) if can_detect(asteroids, a1, a2))

def compute_best_location(asteroids):
    detected_counts = ((a, count_detectable(a, asteroids)) for a in asteroids)
    return max(detected_counts, key=lambda x: x[1])

def compute_angle(a1, a2):
    dx, dy = vsub(a2, a1)
    if dx == 0:
        if dy == 0:
            raise Exception(f'a1 == a2 == {a1}')
        if dy < 0:
            # North
            return (1, 0)
        # South
        return (3, 0)
    if dx > 0:
        # East
        return (2, dy/dx)
    # West
    return (4, dy/dx)

def vaporize_asteroids(asteroids, p):
    angles = [(a, compute_angle(p, a)) for a in asteroids - set([p])]
    sorted_angles = sorted(angles, key=lambda x: x[1])

    asteroids_left = asteroids.copy()
    while sorted_angles:
        next_round = []
        to_remove = []
        for a, angle in sorted_angles:
            if can_detect(asteroids_left, p, a):
                to_remove.append(a)
                yield a
            else:
                next_round.append((a, angle))
        if sorted_angles == next_round:
            raise Exception(f'sorted_angles stayed the same: {sorted_angles}')
        sorted_angles = next_round
        asteroids_left -= set(to_remove)

def compute_day10(input):
    asteroids = parse_asteroids(input)
    best, detected_count = compute_best_location(asteroids)

    gen = vaporize_asteroids(asteroids, best)
    for i in range(199):
        next(gen)
    x200, y200 = next(gen)
    return detected_count, x200*100+y200

if __name__ == '__main__':
    with open('day10.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day10(input)
        print(f'part 1: {p1}, part 2: {p2}')
