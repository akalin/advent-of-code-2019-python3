import itertools

class IntcodeProgram(object):
    def __init__(self, program):
        self.memory = program[:]
        self.ip = 0
        self.halted = False

    def run(self, input, output):
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
            modes_opcode = self.memory[self.ip]
            opcode = modes_opcode % 100
            modes = modes_opcode // 100

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
                    self.ip -= 1
                    return
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

def run_prog_series2(program, phases):
    amp_count = len(phases)
    inputs = [[phases[i]] for i in range(amp_count)]
    inputs[0].append(0)

    programs = [IntcodeProgram(program) for i in range(amp_count)]

    while any(not p.halted for p in programs):
        for i in range(amp_count):
            programs[i].run(inputs[i], inputs[(i+1)%amp_count])

    return inputs[0][0]

def compute_day07(input):
    program = [int(x) for x in input.split(',')]
    return max(run_prog_series2(program, p)
               for p in itertools.permutations(range(5, 10)))

if __name__ == '__main__':
    with open('day07.input', 'r') as input_file:
        input = input_file.read()
        output = compute_day07(input)
        print(f'output: {output}')
