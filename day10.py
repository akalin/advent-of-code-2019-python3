from math import gcd, atan2, pi
from itertools import dropwhile

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
    return max(detected_counts, key=lambda x: x[1])

def compute_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    angle = atan2(dy, dx)
    if angle < -pi/2:
        angle += 2*pi
    return angle

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
                yield a, angle
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
    (x200, y200), _ = next(gen)
    return detected_count, x200*100+y200

if __name__ == '__main__':
    with open('day10.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day10(input)
        print(f'part 1: {p1}, part 2: {p2}')
