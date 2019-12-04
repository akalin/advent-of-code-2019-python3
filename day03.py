#!/Users/akalin/homebrew/bin/python3

from collections import defaultdict

def compute_closest_intersection_helper(input, distance_fn):
    lines = [x.strip() for x in input.strip().split('\n')]
    paths = [line.split(',') for line in lines]

    grid = defaultdict(dict)
    intersections = []

    for wire_no, path in enumerate(paths):
        x, y, step_count = 0, 0, 0
        for segment in path:
            direction = segment[0]
            steps = int(segment[1:])
            if direction == 'U':
                dx = 0
                dy = 1
            elif direction == 'D':
                dx = 0
                dy = -1
            elif direction == 'L':
                dx = -1
                dy = 0
            elif direction == 'R':
                dx = 1
                dy = 0
            else:
                raise Exception(f'Unknown direction {direct}')

            for _ in range(steps):
                x += dx
                y += dy
                step_count += 1
                grid[(x, y)][wire_no] = step_count
                if len(grid[(x, y)]) > 1:
                    intersections.append((x, y, grid[(x, y)]))

    return min([distance_fn(x, y, steps) for x, y, steps in intersections])

def compute_closest_intersection(input, part):
    if part == 1:
        def manhattan_distance(x, y, steps):
            return abs(x) + abs(y)

        return compute_closest_intersection_helper(input, manhattan_distance)
    elif part == 2:
        def step_count(x, y, steps):
            return sum(steps.values())

        return compute_closest_intersection_helper(input, step_count)
    else:
        raise Exception(f'Unknown part {part}')
