from collections import defaultdict, deque
from more_itertools import sliced
from intcode import *

class Node(object):
    def __init__(self, address, program):
        self.address = address
        self.intputer = Intputer(program)
        self.output = []

    def run(self, input):
        if len(self.output) > 0:
            raise
        self.output = self.intputer.run(input)

    def boot(self):
        self.run([self.address])

    def fill_packet_queues(self, packet_queues):
        for dest, x, y in sliced(self.output, 3):
            packet_queues[dest].append((x, y))
        self.output = []

    def drain_packet_queue(self, packet_queues):
        if not self.intputer.waiting_for_input:
            return
        queue = packet_queues[self.address]
        input = []
        if queue:
            for x, y in queue:
                input.extend([x, y])
            queue.clear()
            processed_input = True
        else:
            input = [-1]
            processed_input = False
        self.run(input)
        produced_output = len(self.output) > 0
        return processed_input or produced_output

def compute_day23(input):
    program = parse_intcode(input)
    node_count = 50
    nodes = [Node(i, program) for i in range(node_count)]

    packet_queues = defaultdict(deque)
    nat_queue = packet_queues[255] = deque([], 2)

    for i, node in enumerate(nodes):
        node.boot()

    while True:
        for node in nodes:
            node.fill_packet_queues(packet_queues)

        if len(nat_queue) == 1:
            part1 = nat_queue[0][1]

        did_work = False
        for node in nodes:
            node_did_work = node.drain_packet_queue(packet_queues)
            if node_did_work:
                did_work = True

        if not did_work:
            nat_packet = nat_queue[-1]
            packet_queues[0].append(nat_packet)
            if len(nat_queue) > 1 and nat_packet == nat_queue[0]:
                part2 = nat_packet[1]
                break

    return part1, part2

if __name__ == '__main__':
    with open('day23.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day23(input)
        print(f'part1: {part1}, part2: {part2}')
