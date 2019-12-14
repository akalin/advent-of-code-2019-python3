from intcode import *
from more_itertools import sliced

def count_blocks(program):
    output = []
    Intputer(program).run([], output)
    return len([1 for _, _, c in sliced(output, 3) if c == 2])

def get_initial_game_data(intputer):
    output = []
    intputer.run([], output)
    walls = set()
    blocks = set()
    paddle = None
    ball = None
    score = None
    max_x = 0
    max_y = 0
    for x, y, c in sliced(output, 3):
        if x == -1:
            score = c
            continue

        max_x = max(max_x, x)
        max_y = max(max_y, y)
        if c == 0:
            pass
        elif c == 1:
            walls.add((x, y))
        elif c == 2:
            blocks.add((x, y))
        elif c == 3:
            paddle = (x, y)
        elif c == 4:
            ball = (x, y)
        else:
            raise Exception(f'unknown c={c}')

    return walls, blocks, paddle, ball, score, max_x, max_y

def get_next_paint(intputer, next_input):
    output = []
    intputer.run(next_input, output)
    return {(x, y): c for x, y, c in sliced(output, 3)}

def dump_board(walls, blocks, paddle, ball, width, height):
    grid = []
    for i in range(height):
        grid.append([' '] * width)

    for (x, y) in walls:
        grid[height - y - 1][x] = 'X'

    for (x, y) in blocks:
        grid[height - y - 1][x] = '@'

    (x, y) = paddle
    grid[height - y - 1][x] = '-'

    (x, y) = ball
    grid[height - y - 1][x] = 'o'

    img = '\n'.join(reversed([''.join(row) for row in grid]))
    return img

def run_arcade(program):
    program = program[:]
    program[0] = 2
    intputer = Intputer(program)

    walls, blocks, paddle, ball, score, max_x, max_y = get_initial_game_data(intputer)
    width = max_x + 1
    height = max_y + 1
    img = dump_board(walls, blocks, paddle, ball, width, height)
    print(f'score = {score}, remaining={len(blocks)}')
    print(img)

    while not intputer.halted:
        next_move = 0
        dx2 = ball[0] - paddle[0]
        if dx2 > 0:
            next_move = 1
            paddle = (paddle[0] + 1, paddle[1])
        elif dx2 < 0:
            next_move = -1
            paddle = (paddle[0] - 1, paddle[1])
        paint = get_next_paint(intputer, [next_move])

        for p, c in paint.items():
            if p[0] == -1:
                score = c
            elif c == 0:
                blocks.discard(p)
            elif c == 3:
                paddle = p
            elif c == 4:
                ball = p
            else:
                raise Exception(f'unexpected c={c}')

        img = dump_board(walls, blocks, paddle, ball, width, height)
        print(f'score = {score}, remaining={len(blocks)}')
        print(img)

    if blocks:
        raise(f'blocks unexpectedly non-empty: {blocks}')
    return score

def compute_day13(input):
    program = parse_intcode(input)
    part1 = count_blocks(program)
    part2 = run_arcade(program)
    return part1, part2

if __name__ == '__main__':
    with open('day13.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day13(input)
        print(f'part1: {part1}, part2: {part2}')
