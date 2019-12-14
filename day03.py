from collections import defaultdict
from util import *
from vec2 import *

def compute_closest_intersection(input):
    lines = [x.strip() for x in input.strip().split('\n')]
    paths = [line.split(',') for line in lines]

    grid = defaultdict(dict)

    for wire_no, path in enumerate(paths):
        p = Vec2(0, 0)
        step_count = 0
        for segment in path:
            direction = segment[0]
            steps = int(segment[1:])
            if direction == 'U':
                dp = (0, 1)
            elif direction == 'D':
                dp = (0, -1)
            elif direction == 'L':
                dp = (-1, 0)
            elif direction == 'R':
                dp = (1, 0)
            else:
                raise Exception(f'Unknown direction {direction}')

            for _ in range(steps):
                p += dp
                step_count += 1
                if wire_no not in grid[p]:
                    grid[p][wire_no] = step_count

    intersections = [(p, steps) for p, steps in grid.items() if len(steps) > 1]

    min_manhattan_distance = min([manhattan_norm(p) for p, _ in intersections])
    min_step_count = min([sum(steps.values()) for _, steps in intersections])
    return min_manhattan_distance, min_step_count

if __name__ == '__main__':
    with open('day03.input', 'r') as input_file:
        input = input_file.read()
        min_manhattan_distance, min_step_count = compute_closest_intersection(input)
        print(f'min manhattan distance: {min_manhattan_distance}, min step count: {min_step_count}')
