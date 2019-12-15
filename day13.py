from intcode import *
from util import *
from more_itertools import sliced
import os

def count_blocks(program):
    output = []
    Intputer(program).run([], output)
    return len([c for _, _, c in sliced(output, 3) if c == 2])

def maybe_show_game(walls, blocks, paddle, ball, score):
    show_game = True
    if not show_game:
        return

    canvas = ASCIICanvas()
    canvas.put_set(walls, 'X')
    canvas.put_set(blocks, '@')
    canvas.put(paddle, '-')
    canvas.put(ball, 'o')

    os.system('clear')
    print(f'score = {score}, remaining={len(blocks)}')
    print(canvas.render())

def play_game(program):
    program = program[:]
    program[0] = 2
    intputer = Intputer(program)

    output = []
    intputer.run([], output)
    walls = set()
    blocks = set()
    paddle = None
    ball = None
    score = None
    for x, y, c in sliced(output, 3):
        if x == -1:
            score = c
            continue

        p = (x, y)
        if c == 0:
            pass
        elif c == 1:
            walls.add(p)
        elif c == 2:
            blocks.add(p)
        elif c == 3:
            paddle = p
        elif c == 4:
            ball = p
        else:
            raise Exception(f'unknown c={c}')

    maybe_show_game(walls, blocks, paddle, ball, score)

    while not intputer.halted:
        next_move = 0
        dx2 = ball[0] - paddle[0]
        if dx2 > 0:
            next_move = 1
            paddle = (paddle[0] + 1, paddle[1])
        elif dx2 < 0:
            next_move = -1
            paddle = (paddle[0] - 1, paddle[1])

        output = []
        intputer.run([next_move], output)
        for x, y, c in sliced(output, 3):
            if x == -1:
                score = c
                continue

            p = (x, y)
            if c == 0:
                blocks.discard(p)
            elif c == 3:
                paddle = p
            elif c == 4:
                ball = p
            else:
                raise Exception(f'unexpected c={c}')

        maybe_show_game(walls, blocks, paddle, ball, score)

    if blocks:
        raise(f'blocks unexpectedly non-empty: {blocks}')
    return score

def compute_day13(input):
    program = parse_intcode(input)
    part1 = count_blocks(program)
    part2 = play_game(program)
    return part1, part2

if __name__ == '__main__':
    with open('day13.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day13(input)
        print(f'part1: {part1}, part2: {part2}')
