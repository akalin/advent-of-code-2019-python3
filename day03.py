from collections import defaultdict

def compute_closest_intersection(input):
    lines = [x.strip() for x in input.strip().split('\n')]
    paths = [line.split(',') for line in lines]

    grid = defaultdict(dict)

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
                raise Exception(f'Unknown direction {direction}')

            for _ in range(steps):
                x += dx
                y += dy
                step_count += 1
                if wire_no not in grid[(x, y)]:
                    grid[(x, y)][wire_no] = step_count

    intersections = [(x, y, steps) for (x, y), steps in grid.items() if len(steps) > 1]

    min_manhattan_distance = min([abs(x) + abs(y) for x, y, _ in intersections])
    min_step_count = min([sum(steps.values()) for _, _, steps in intersections])
    return min_manhattan_distance, min_step_count

if __name__ == '__main__':
    with open('day03.input', 'r') as input_file:
        input = input_file.read()
        min_manhattan_distance, min_step_count = compute_closest_intersection(input)
        print(f'min manhattan distance: {min_manhattan_distance}, min step count: {min_step_count}')
