import collections
import itertools

class Intputer(object):
    def __init__(self, program):
        self.memory = collections.defaultdict(int, enumerate(program))
        self.ip = 0
        self.rel_base = 0
        self.waiting_for_input = False
        self.halted = False

    def run(self, input):
        if self.halted:
            raise Exception('Called run when halted')

        if self.waiting_for_input and len(input) == 0:
            raise Exception('Called run with empty input while waiting for input')

        output = []
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
                    break
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
                break

            else:
                raise Exception(f'Unknown opcode {opcode}')

        return output

def run(program, input):
    intputer = Intputer(program)
    output = intputer.run([input])
    return output[0]

def compute_day09(input):
    program = [int(x) for x in input.split(',')]
    return run(program, 1), run(program, 2)

if __name__ == '__main__':
    with open('day09.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day09(input)
        print(f'part1: {part1}, part2: {part2}')
