def run_prog(program, input):
    memory = program[:]

    ip = 0
    input_pos = 0
    output = []
    modes = 0
    nargs = 0

    def compute_mode(i):
        return (modes // (10**i)) % 10

    def check_i(i):
        if i >= nargs:
            raise Exception(f'i={i} >= nargs={nargs}')

    def getp(i):
        check_i(i)
        p = memory[ip+i]
        mode = compute_mode(i)
        if mode == 0:
            # position mode
            return memory[p]
        if mode == 1:
            # immediate mode
            return p
        raise Exception(f'Unknown mode {mode}')

    def setp(i, v):
        check_i(i)
        mode = compute_mode(i)
        if mode != 0:
            raise Exception(f'Unexpected mode {mode} for setp')
        p = memory[ip+i]
        memory[p] = v

    def adv():
        nonlocal ip
        ip += nargs

    while True:
        modes, opcode = divmod(memory[ip], 100)
        ip += 1

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
            setp(0, input[input_pos])
            input_pos += 1
            adv()

        elif opcode == 4:
            # Produce output
            nargs = 1
            output.append(getp(0))
            adv()

        elif opcode == 5:
            # jne
            nargs = 2
            if getp(0) != 0:
                ip = getp(1)
            else:
                adv()

        elif opcode == 6:
            # jeq
            nargs = 2
            if getp(0) == 0:
                ip = getp(1)
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
            break

        else:
            raise Exception(f'Unknown opcode {opcode}')
    return memory, output

def compute_day05(input):
    program = [int(x) for x in input.split(',')]
    _, part1 = run_prog(program, [1])
    _, part2 = run_prog(program, [5])
    return part1, part2

if __name__ == '__main__':
    with open('day05.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day05(input)
        print(f'part 1: {part1}, part 2: {part2}')
