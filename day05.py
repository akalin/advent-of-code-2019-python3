def run_prog(program, input):
    memory = program[:]

    ip = 0
    np = 0
    output = []
    while True:
        opcode = memory[ip] % 100
        modes = [
            (memory[ip] // 100) % 10,
            (memory[ip] // 1000) % 10,
            (memory[ip] // 10000) % 10,
        ]
        def get_param(i):
            p = memory[ip+i+1]
            if modes[i] == 0:
                return memory[p]
            if modes[i] == 1:
                return p
            raise Exception(f'Unknown mode {modes[i]}')
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
                print(f'setting ip to {get_param(1)}')
                ip = get_param(1)
            else:
                ip += 3
        elif opcode == 6:
            if get_param(0) == 0:
                print(f'setting ip to {get_param(1)}')
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
    return run_prog(input, [5])

if __name__ == '__main__':
    y = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    ints = [int(x) for x in y.split(',')]
    x = run_prog(ints, [1])
    print(f'x {x}')
    with open('day05.input', 'r') as input_file:
        input = input_file.read()
        ints = [int(x) for x in input.split(',')]
        output = compute_day05(ints)
        print(f'output: {output}')
