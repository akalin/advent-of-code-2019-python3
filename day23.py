from collections import defaultdict, deque
from more_itertools import chunked
import itertools
from intcode import *
from util import *
from vec2 import *

class Node(object):
    def __init__(self, address, program):
        self.address = address
        self.intputer = Intputer(program)
        self.input = deque()
        self.output = deque()

    def run(self):
        self.intputer.run_deque(self.input, self.output)

    def boot(self):
        self.input.append(self.address)
        self.run()

    def fill_packet_queues(self, packet_queues):
        for dest, x, y in chunked(self.output, 3):
            packet_queues[dest].append((x, y))
        self.output.clear()

    def drain_packet_queue(self, packet_queues):
        if not self.intputer.waiting_for_input:
            return
        queue = packet_queues[self.address]
        if queue:
            for x, y in queue:
                self.input.extend([x, y])
            queue.clear()
            processed_input = True
        else:
            self.input.append(-1)
            processed_input = False
        self.run()
        produced_output = len(self.output) > 0
        return processed_input or produced_output

def compute_day23(input):
    program = parse_intcode(input)
    node_count = 50
    nodes = [Node(i, program) for i in range(node_count)]

    packet_queues = defaultdict(deque)

    nat_packet = None
    last_nat_packet = None

    for i, node in enumerate(nodes):
        node.boot()

    while True:
        for node in nodes:
            node.fill_packet_queues(packet_queues)

        did_work = False
        for node in nodes:
            node_did_work = node.drain_packet_queue(packet_queues)
            if node_did_work:
                did_work = True

        if packet_queues[255]:
            nat_packet = packet_queues[255][-1]
            print(f'setting nat packet to {nat_packet}')
            packet_queues[255].clear()

        if not did_work:
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
