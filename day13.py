from intcode import *
from more_itertools import sliced

def get_next_paint(intputer, next_input):
    output = []
    intputer.run(next_input, output)
    return {(x, y): c for x, y, c in sliced(output, 3)}

def update_game_data(paint, walls, blocks, paddle, ball, score):
    next_walls = walls.copy()
    next_blocks = blocks.copy()
    next_paddle = paddle
    next_ball = ball
    next_score = score
    for p, c in paint.items():
        if p[0] == -1:
            next_score = c
        elif c == 0:
            next_walls.discard(p)
            next_blocks.discard(p)
        elif c == 1:
            next_walls.add(p)
            next_blocks.discard(p)
        elif c == 2:
            next_walls.discard(p)
            next_blocks.add(p)
        elif c == 3:
            next_paddle = p
        elif c == 4:
            next_ball = p
        else:
            raise Exception(f'unknown c={c}')

    return next_walls, next_blocks, next_paddle, next_ball, next_score

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
    program[0] = 2
    intputer = Intputer(program)
    output = []

    initial_paint = get_next_paint(intputer, [])
    width = 1 + max([x for x, _ in initial_paint.keys()])
    height = 1 + max([y for _, y in initial_paint.keys()])

    walls = set()
    blocks = set()
    paddle = None
    ball = None
    score = None
    walls, blocks, paddle, ball, score = update_game_data(initial_paint, walls, blocks, paddle, ball, score)
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
        walls, blocks, paddle, ball, score = update_game_data(paint, walls, blocks, paddle, ball, score)
        img = dump_board(walls, blocks, paddle, ball, width, height)
        print(f'score = {score}, remaining={len(blocks)}')
        print(img)

    if blocks:
        raise(f'blocks unexpectedly non-empty: {blocks}')
    return score

def compute_day13(input):
    program = parse_intcode(input)
    part2 = run_arcade(program)
    return None, part2

if __name__ == '__main__':
    with open('day13.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day13(input)
        print(f'part1: {part1}, part2:\n{part2}')
