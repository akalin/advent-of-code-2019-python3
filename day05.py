def run_prog(program, input):
    memory = program[:]

    ip = 0
    np = 0
    output = []

    def getp(i):
        p = memory[ip+i+1]
        mode = (memory[ip] // (10**(i+2))) % 10
        if mode == 0:
            # position mode
            return memory[p]
        if mode == 1:
            # immediate mode
            return p
        raise Exception(f'Unknown mode {mode}')

    def setp(i, v):
        # TODO: Assert mode is position.
        p = memory[ip+i+1]
        memory[p] = v

    # np = parameter count
    def adv(np):
        nonlocal ip
        ip += np + 1

    while True:
        opcode = memory[ip] % 100

        if opcode == 1:
            # Add
            setp(2, getp(0) + getp(1))
            adv(3)

        elif opcode == 2:
            # Multiply
            setp(2, getp(0) * getp(1))
            adv(3)

        elif opcode == 3:
            # Consume input
            setp(0, input[np])
            np += 1
            adv(1)

        elif opcode == 4:
            # Produce output
            output.append(getp(0))
            adv(1)

        elif opcode == 5:
            # jne
            if getp(0) != 0:
                ip = getp(1)
            else:
                adv(2)

        elif opcode == 6:
            # jeq
            if getp(0) == 0:
                ip = getp(1)
            else:
                adv(2)

        elif opcode == 7:
            # lt
            setp(2, int(getp(0) < getp(1)))
            adv(3)

        elif opcode == 8:
            # eq
            setp(2, int(getp(0) == getp(1)))
            adv(3)

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
