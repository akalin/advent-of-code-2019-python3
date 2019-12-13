import collections
import itertools

class Intputer(object):
    def __init__(self, program):
        self.memory = collections.defaultdict(int, enumerate(program))
        self.ip = 0
        self.rel_base = 0
        self.waiting_for_input = False
        self.halted = False

    def run(self, input, output):
        if self.halted:
            raise Exception('Called run when halted')

        if self.waiting_for_input and len(input) == 0:
            raise Exception('Called run with empty input while waiting for input')

        modes = []
        nargs = 0

        def check_i(i):
            if i >= nargs:
                raise Exception(f'i={i} >= nargs={nargs}')

        def getmem(i):
            if i < 0:
                raise Exception(f'getmem: Invalid address {i}')
            return self.memory[i]

        def setmem(i, v):
            if i < 0:
                raise Exception(f'setmem: invalid address {i}')
            self.memory[i] = v

        def getp(i):
            check_i(i)
            p = getmem(self.ip+i)
            mode = modes[i]
            if mode == 0:
                # position mode
                return getmem(p)
            if mode == 1:
                # immediate mode
                return p
            if mode == 2:
                # relative mode
                return getmem(self.rel_base + p)
            raise Exception(f'Unexpected mode {mode} for getp')

        def setp(i, v):
            check_i(i)
            mode = modes[i]
            p = getmem(self.ip+i)
            if mode == 0:
                # position mode
                setmem(p, v)
                return
            if mode == 2:
                # relative mode
                setmem(self.rel_base + p, v)
                return
            raise Exception(f'Unexpected mode {mode} for setp')

        def adv():
            self.ip += nargs

        while True:
            modes_int, opcode = divmod(getmem(self.ip), 100)
            modes = [0, 0, 0]
            modes_int, modes[0] = divmod(modes_int, 10)
            modes_int, modes[1] = divmod(modes_int, 10)
            modes_int, modes[2] = divmod(modes_int, 10)
            if modes_int != 0:
                raise Exception(f'modes_int={modes_int} unexpectedly non-zero')

            self.ip += 1

            if opcode == 1:
                # Add
                nargs = 3
                setp(2, getp(0) + getp(1))
                adv()

            elif opcode == 2:
                # Multiply
                nargs = 3
                setp(2, getp(0) * getp(1))
                adv()

            elif opcode == 3:
                # Consume input
                nargs = 1
                if len(input) == 0:
                    self.waiting_for_input = True
                    self.ip -= 1
                    return
                self.waiting_for_input = False
                v = input.pop(0)
                setp(0, v)
                adv()

            elif opcode == 4:
                # Produce output
                nargs = 1
                v = getp(0)
                output.append(v)
                adv()

            elif opcode == 5:
                # jne
                nargs = 2
                if getp(0) != 0:
                    self.ip = getp(1)
                else:
                    adv()

            elif opcode == 6:
                # jeq
                nargs = 2
                if getp(0) == 0:
                    self.ip = getp(1)
                else:
                    adv()

            elif opcode == 7:
                # lt
                nargs = 3
                setp(2, int(getp(0) < getp(1)))
                adv()

            elif opcode == 8:
                # eq
                nargs = 3
                setp(2, int(getp(0) == getp(1)))
                adv()

            elif opcode == 9:
                # Adjust relative base
                nargs = 1
                self.rel_base += getp(0)
                adv()

            elif opcode == 99:
                # halt
                self.halted = True
                return

            else:
                raise Exception(f'Unknown opcode {opcode}')

def run_game(intputer, next_input):
    output = []
    intputer.run(next_input, output)

    empty_tiles = set()
    walls = set()
    blocks = set()
    paddle = None
    ball = None
    score = None

    max_x = 0
    max_y = 0
    for i in range(0, len(output), 3):
        x = output[i]
        y = output[i+1]
        if x != -1:
            max_x = max(max_x, x)
        max_y = max(max_y, y)
        c = output[i+2]
        if x == -1:
            score = c
        elif c == 0:
            empty_tiles.add((x, y))
        elif c == 1:
            walls.add((x, y))
        elif c == 2:
            blocks.add((x, y))
        elif c == 3:
            paddle = (x, y)
        elif c == 4:
            ball = (x, y)
        else:
            raise Exception(f'what, c={c}')

    return walls, blocks, paddle, ball, score, max_x, max_y

def dump_board(walls, blocks, paddle, ball, max_x, max_y):
    grid = []
    for i in range(max_y+1):
        grid.append([' '] * (max_x+1))

    for (x, y) in walls:
        grid[max_y - y][x] = 'X'

    for (x, y) in blocks:
        grid[max_y - y][x] = '@'

    (x, y) = paddle
    grid[max_y - y][x] = '-'

    (x, y) = ball
    grid[max_y - y][x] = 'o'

    img = '\n'.join(reversed([''.join(row) for row in grid]))
    return img

def run_arcade(program):
    program[0] = 2
    intputer = Intputer(program)
    output = []

    walls, blocks, paddle, ball, score, max_x, max_y = run_game(intputer, [])
    img = dump_board(walls, blocks, paddle, ball, max_x, max_y)
    print(f'score = {score}, remaining={len(blocks)}')
    print(img)

    next_input = []
    while ball != max_y and not intputer.halted:
        next_move = 0
        dx2 = ball[0] - paddle[0]
        if dx2 > 0:
            next_move = 1
            paddle = (paddle[0] + 1, paddle[1])
        elif dx2 < 0:
            next_move = -1
            paddle = (paddle[0] - 1, paddle[1])
        _, _, _, ball2, score2, _, _ = run_game(intputer, [next_move])
        if ball2:
            if ball2 in blocks:
                blocks.remove(ball2)
            ball = ball2
        if score2 is not None:
            score = score2
        img = dump_board(walls, blocks, paddle, ball, max_x, max_y)
        print(f'score = {score}, remaining={len(blocks)}')
        print(img)

    return None

def compute_day13(input):
    program = [int(x) for x in input.split(',')]
    output = run_arcade(program)
    return output, None

if __name__ == '__main__':
    with open('day13.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day13(input)
        print(f'part1: {part1}, part2:\n{part2}')
