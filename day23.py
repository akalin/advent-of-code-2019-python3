from collections import defaultdict
from more_itertools import sliced
import itertools
from intcode import *
from util import *
from vec2 import *

def compute_day23(input):
    program = parse_intcode(input)
    int_count = 50
    intputers = [Intputer(program) for _ in range(int_count)]
    inputs = [[i] for i in range(int_count)]
    outputs = [[] for _ in range(int_count)]

    packet_queues = defaultdict(list)

    nat_packet = None
    last_nat_packet = None

    for i, intputer in enumerate(intputers):
        intputer.run(inputs[i], outputs[i])

    while True:
        for output in outputs:
            for dest, x, y in sliced(output, 3):
                packet_queues[dest].append((x, y))
            output.clear()

#        for i, intputer in enumerate(intputers):
#            print(i, inputs[i], outputs[i], intputer.halted, intputer.waiting_for_input)

        idle = True
        for i, intputer in enumerate(intputers):
            if not intputer.waiting_for_input:
                continue
            queue = packet_queues[i]
            if queue:
                for x, y in queue:
                    inputs[i].append(x)
                    inputs[i].append(y)
                queue.clear()
                idle = False
            else:
                inputs[i].append(-1)
            intputer.run(inputs[i], outputs[i])

        for output in outputs:
            if len(output) > 0:
                idle = False


        if packet_queues[255]:
            nat_packet = packet_queues[255][-1]
            print(f'setting nat packet to {nat_packet}')
            packet_queues[255].clear()

        if idle:
            print(f'is idle, nat packet is {nat_packet}')
            if nat_packet is None:
                raise
            packet_queues[0].append(nat_packet)
            if nat_packet == last_nat_packet:
                break
            last_nat_packet = nat_packet

    return None, None

if __name__ == '__main__':
    with open('day23.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day23(input)
        print(f'part1: {part1}, part2: {part2}')
