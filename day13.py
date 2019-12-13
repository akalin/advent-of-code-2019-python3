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

def do_turn(dir, turn):
    if turn == 0:
        if dir == 'U':
            return 'L'
        if dir == 'L':
            return 'D'
        if dir == 'D':
            return 'R'
        if dir == 'R':
            return 'U'
    else:
        if dir == 'U':
            return 'R'
        if dir == 'R':
            return 'D'
        if dir == 'D':
            return 'L'
        if dir == 'L':
            return 'U'

def move_forward(pos, dir):
    if dir == 'U':
        return (pos[0] + 1, pos[1])
    if dir == 'D':
        return (pos[0] - 1, pos[1])
    if dir == 'L':
        return (pos[0], pos[1] - 1)
    if dir == 'R':
        return (pos[0], pos[1] + 1)

def run_arcade(program, initial_color):
    program[0] = 2
    intputer = Intputer(program)
    grid = collections.defaultdict(int)
    pos = (0, 0)
    grid[pos] = initial_color
    output = []
    intputer.run([0, 0, 0], output)
    for i in range(0, len(output), 3):
        x = output[i]
        y = output[i+1]
        btype = output[i+2]
        grid[(x, y)] = btype
    min_x = min([x for x, y in grid.keys()])
    max_x = max([x for x, y in grid.keys()])
    min_y = min([y for x, y in grid.keys()])
    max_y = max([y for x, y in grid.keys()])
    grid2 = []
    xlen = max_x - min_x + 1
    ylen = max_y - min_y + 1
    for i in range(ylen):
        grid2.append([' '] * xlen)
    for (x, y), c in grid.items():
        xx = x - min_x
        yy = ylen - (y - min_y) - 1
        if c == 0:
            d = ' '
        elif c == 1:
            d = 'X'
        elif c == 2:
            d = '.'
        elif c == 3:
            d = '*'
        elif c == 4:
            d = 'o'
        else:
            raise Exception(f'what {c}')
        grid2[yy][xx] = d
    img = '\n'.join(reversed([''.join(row) for row in grid2]))
    print(img)
    return None

def compute_day13(input):
    program = [int(x) for x in input.split(',')]
    output = run_arcade(program, 0)
    return output, None

if __name__ == '__main__':
    with open('day13.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day13(input)
        print(f'part1: {part1}, part2:\n{part2}')
