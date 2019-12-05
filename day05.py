def run_prog(program, input):
    memory = program[:]

    ip = 0
    np = 0
    output = []
    while True:
        def get_param(i):
            p = memory[ip+i+1]
            mode = (memory[ip] // (10**(i+2))) % 10
            if mode == 0:
                return memory[p]
            if mode == 1:
                return p
            raise Exception(f'Unknown mode {modes[i]}')

        opcode = memory[ip] % 100

        if opcode == 1:
            p3 = memory[ip+3]
            memory[p3] = get_param(0) + get_param(1)
            ip += 4
        elif opcode == 2:
            p3 = memory[ip+3]
            memory[p3] = get_param(0) * get_param(1)
            ip += 4
        elif opcode == 3:
            p1 = memory[ip+1]
            memory[p1] = input[np]
            np += 1
            ip += 2
        elif opcode == 4:
            output.append(get_param(0))
            ip += 2
        elif opcode == 5:
            if get_param(0) != 0:
                ip = get_param(1)
            else:
                ip += 3
        elif opcode == 6:
            if get_param(0) == 0:
                ip = get_param(1)
            else:
                ip += 3
        elif opcode == 7:
            p3 = memory[ip+3]
            if get_param(0) < get_param(1):
                memory[p3] = 1
            else:
                memory[p3] = 0
            ip += 4
        elif opcode == 8:
            p3 = memory[ip+3]
            if get_param(0) == get_param(1):
                memory[p3] = 1
            else:
                memory[p3] = 0
            ip += 4
        elif opcode == 99:
            break
        else:
            raise Exception(f'Unknown opcode {opcode}')
    return output

def compute_day05(input):
    program = [int(x) for x in input.split(',')]
    part1 = run_prog(program, [1])
    part2 = run_prog(program, [5])
    return part1, part2

if __name__ == '__main__':
    with open('day05.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day05(input)
        print(f'part 1: {part1}, part 2: {part2}')
