import itertools

class Intputer(object):
    def __init__(self, program):
        self.memory = program[:]
        self.ip = 0
        self.waiting_for_input = False
        self.halted = False

    def run(self, input, output):
        if self.halted:
            raise Exception('Called run when halted')

        if self.waiting_for_input and len(input) == 0:
            raise Exception('Called run with empty input while waiting for input')

        modes = 0
        nargs = 0

        def compute_mode(i):
            return (modes // (10**i)) % 10

        def check_i(i):
            if i >= nargs:
                raise Exception(f'i={i} >= nargs={nargs}')

        def getp(i):
            check_i(i)
            p = self.memory[self.ip+i]
            mode = compute_mode(i)
            if mode == 0:
                # position mode
                return self.memory[p]
            if mode == 1:
                # immediate mode
                return p
            raise Exception(f'Unknown mode {mode}')

        def setp(i, v):
            check_i(i)
            mode = compute_mode(i)
            if mode != 0:
                raise Exception(f'Unexpected mode {mode} for setp')
            p = self.memory[self.ip+i]
            self.memory[p] = v

        def adv():
            self.ip += nargs

        while True:
            modes, opcode = divmod(self.memory[self.ip], 100)

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

            elif opcode == 99:
                # halt
                self.halted = True
                return

            else:
                raise Exception(f'Unknown opcode {opcode}')

def run_serial_mode(program, phases):
    pipes = [[p] for p in phases] + [[]]
    pipes[0].append(0)

    for input, output in zip(pipes, pipes[1:]):
        Intputer(program).run(input, output)

    return pipes[-1][0]

def run_feedback_mode(program, phases):
    pipes = [[p] for p in phases]
    pipes[0].append(0)

    intputers = [Intputer(program) for _ in range(len(phases))]

    while not intputers[-1].halted:
        for i, intputer in enumerate(intputers):
            intputer.run(pipes[i], pipes[(i+1)%len(pipes)])

    return pipes[0][0]

def compute_day07(input):
    program = [int(x) for x in input.split(',')]

    max_serial = max(run_serial_mode(program, p)
                     for p in itertools.permutations(range(5)))
    max_feedback = max(run_feedback_mode(program, p)
                       for p in itertools.permutations(range(5, 10)))
    return max_serial, max_feedback

if __name__ == '__main__':
    with open('day07.input', 'r') as input_file:
        input = input_file.read()
        max_serial, max_feedback = compute_day07(input)
        print(f'max serial: {max_serial}, max feedback: {max_feedback}')
