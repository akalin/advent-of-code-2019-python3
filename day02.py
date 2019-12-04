#!/Users/akalin/homebrew/bin/python3

def run_prog(program, noun, verb):
    memory = program[:]
    memory[1] = noun
    memory[2] = verb

    ip = 0
    while True:
        opcode = memory[ip]
        if opcode == 1:
            p1, p2, p3 = memory[ip+1:ip+4]
            memory[p3] = memory[p1] + memory[p2]
            ip += 4
        elif opcode == 2:
            p1, p2, p3 = memory[ip+1:ip+4]
            memory[p3] = memory[p1] * memory[p2]
            ip += 4
        elif opcode == 99:
            break
        else:
            raise Exception(f'Unknown opcode {opcode}')
    return memory

puzzleInput = '''1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,5,19,23,1,23,6,27,1,5,27,31,1,31,6,35,1,9,35,39,2,10,39,43,1,43,6,47,2,6,47,51,1,5,51,55,1,55,13,59,1,59,10,63,2,10,63,67,1,9,67,71,2,6,71,75,1,5,75,79,2,79,13,83,1,83,5,87,1,87,9,91,1,5,91,95,1,5,95,99,1,99,13,103,1,10,103,107,1,107,9,111,1,6,111,115,2,115,13,119,1,10,119,123,2,123,6,127,1,5,127,131,1,5,131,135,1,135,6,139,2,139,10,143,2,143,9,147,1,147,6,151,1,151,13,155,2,155,9,159,1,6,159,163,1,5,163,167,1,5,167,171,1,10,171,175,1,13,175,179,1,179,2,183,1,9,183,0,99,2,14,0,0'''

ints_orig = [int(x) for x in puzzleInput.split(',')]

for n in range(0, 100):
    for v in range(0, 100):
        res = run_prog(ints_orig, n, v)
        if res[0] == 19690720:
            print(f'n={n}, v={v}, 100*n+v={100*n+v}')
