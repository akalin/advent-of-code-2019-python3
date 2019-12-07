def run_prog(id, program, ip, input, output):
    memory = program[:]

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
        opcode = memory[ip] % 100
        modes = memory[ip] // 100
        print(f'{id} is at ip {ip} opcode {opcode}')

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
            if len(input) == 0:
                print(f'{id} need input, ip {ip-1}')
                return 'need input', memory, ip-1
            v = input.pop(0)
            print(f'{id} consuming input {v}, len={len(input)}')
            setp(0, v)
            adv()
            print(f'{id} ip is now {ip}')

        elif opcode == 4:
            # Produce output
            nargs = 1
            v = getp(0)
            output.append(v)
            print(f'{id} producing output {v}, len={len(output)}')
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
    return 'halt', memory, None

def run_prog_series2(program, phases):
    signal = 0

    amp_count = len(phases)
    inputs = [[phases[i]] for i in range(amp_count)]
    inputs[0].append(0)

    programs = [program[:] for i in range(amp_count)]
    ips = [0 for i in range(amp_count)]
    running = [True for i in range(amp_count)]

    while any(running):
        for i in range(amp_count):
            print(f'running {i} with ip {ips[i]} and input length {len(inputs[i])}')
            state, mem, ip = run_prog(i, programs[i], ips[i], inputs[i], inputs[(i+1)%amp_count])
            if state == 'need input':
                print(f'{i} needs input, got ip {ip}')
                programs[i] = mem
                ips[i] = ip
            elif state == 'halt':
                running[i] = False
            else:
                raise Exception(f'Unknown state {state}')

    return inputs[0][0]

def compute_day07(input):
    program = [int(x) for x in input.split(',')]
    max_output = 0
    for i1 in range(5,10):
        for i2 in range(5,10):
            if i2 == i1:
                continue
            for i3 in range(5,10):
                if i3 == i1 or i3 == i2:
                    continue
                for i4 in range(5,10):
                    if i4 == i1 or i4 == i2 or i4 == i3:
                        continue
                    for i5 in range(5,10):
                        if i5 == i1 or i5 == i2 or i5 == i3 or i5 == i4:
                            continue
                        output = run_prog_series2(program, [i1, i2, i3, i4, i5])
                        if output > max_output:
                            max_output = output
    return max_output

if __name__ == '__main__':
    program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    output = run_prog_series2(program, [9,8,7,6,5])
    print(output)

    program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    output = run_prog_series2(program, [9,7,8,5,6])
    print(output)

    with open('day07.input', 'r') as input_file:
        input = input_file.read()
        output = compute_day07(input)
        print(f'output: {output}')
