from collections import deque
import itertools
from intcode import *
from util import *
from vec2 import *
from vec3 import *

def deal_new_stack(deck):
    return list(reversed(deck))

def cut_cards(deck, n):
    return deck[n:] + deck[:n]

def deal_increment(deck, n):
    new_deck = [0] * len(deck)
    for i, c in enumerate(deck):
        j = (i * n) % len(deck)
        new_deck[j] = c
    return new_deck

def compute_day22(input):
    count = 10007
    deck = [i for i in range(count)]
    lines = [x for x in input.split('\n')]
    print(lines)
    for line in lines:
        if len(line) == 0:
            continue
        words = line.split(' ')
        print(words)
        if words[0] == 'cut':
            n = int(words[1])
            print('cut', n)
            deck = cut_cards(deck, n)
        elif words[0] == 'deal' and words[1] == 'with':
            n = int(words[3])
            print('with', n)
            deck = deal_increment(deck, n)
        elif words[0] == 'deal' and words[1] == 'into':
            print('deal into')
            deck = deal_new_stack(deck)

    print(deck)
    for i, c in enumerate(deck):
        if c == 2019:
            print(i)

    return None, None

if __name__ == '__main__':
    with open('day22.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day22(input)
        print(f'part1: {part1}, part2: {part2}')
