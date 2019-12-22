from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *
from vec3 import *

def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
  
        # q is quotient 
        q = a // m 
  
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return x

# 7*(i + c)
# 7*i + 0
# -7*(i - 1)
class Deck(object):
    def __init__(self, count):
        self.count = count
        self.factor = 1
        self.offset = 0

    def get(self, i):
        j = (self.factor*i + self.offset) % self.count
        return j

    def deal_new(self):
        self.offset = self.get(-1)
        self.factor = (self.factor * -1) % self.count
#        print('new', self.factor, self.offset)

    def cut(self, n):
        self.offset = self.get(n)
#        print('cut', self.factor, self.offset)

    def deal_increment(self, n):
        n_inv = modInverse(n, self.count)
        self.factor = (self.factor * n_inv) % self.count
#        print('inc', self.factor, self.offset)

    def to_list(self):
        l = [0] * self.count
        for i in range(self.count):
            l[i] = self.get(i)
        return l

    def do_shuffle(self, lines):
        for line in lines:
            if len(line) == 0:
                continue
            words = line.split(' ')
            if words[0] == 'cut':
                n = int(words[1])
                self.cut(n)
            elif words[0] == 'deal' and words[1] == 'with':
                n = int(words[3])
                self.deal_increment(n)
            elif words[0] == 'deal' and words[1] == 'into':
                self.deal_new()

    def square(self):
        new_factor = (self.factor * self.factor) % self.count
        new_offset = (self.offset * self.factor + self.offset) % self.count
        self.factor = new_factor
        self.offset = new_offset

#            print(self.to_list())

def compute_day22(input):
    count = 119315717514047
#    count = 10007
#    count = 10
    deck = Deck(count)
    lines = [x for x in input.split('\n')]

    deck.do_shuffle(lines)
    print(f'c={deck.count} fac={deck.factor} off={deck.offset}')

    # a(ax + b) + b
    # a^2x + ab + b
    new_factor = (deck.factor * deck.factor) % deck.count
    new_offset = (deck.offset * deck.factor + deck.offset) % deck.count

    print(f'fac={new_factor} off={new_offset}')

#    for i in range(101741582076661):
    deck.square()
    print(f'c={deck.count} fac={deck.factor % deck.count} off={deck.offset % deck.count}')

#    for i in range(count):
#        if deck.get(i) == 2019:
#            print(i)
    print(deck.get(2020))
    return None, None

if __name__ == '__main__':
    with open('day22.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day22(input)
        print(f'part1: {part1}, part2: {part2}')
