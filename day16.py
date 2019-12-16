import collections
from intcode import *
from util import *
from vec2 import *
from vec3 import *

base_pattern = [0, 1, 0, -1]

def get_pattern(num_count, i):
    pattern = []
    pi = 0
    while len(pattern) < num_count+1:
        n = base_pattern[pi]
        pattern += [n] * (i + 1)
        pi = (pi + 1) % len(base_pattern)
    return pattern[1:num_count+1]

def compute_ith(nums_in, i):
    pattern = get_pattern(len(nums_in), i)
    s = sum([a * b for a, b in zip(nums_in, pattern)])
    s = abs(s) % 10
    return s

def do_round(nums_in):
    nums_out = [compute_ith(nums_in, i) for i in range(len(nums_in))]
    return nums_out

def apply_fft(nums_in, rounds):
    nums_out = nums_in
    for i in range(rounds):
        nums_out = do_round(nums_out)
    return nums_out

def do_round_second_half(nums):
    s = 0
    for i in range(1, len(nums) + 1):
        s = (s + nums[-i]) % 10
        nums[-i] = s

def apply_fft_second_half(nums_in, rounds):
    nums_out = nums_in
    for i in range(rounds):
        print(i)
        do_round_second_half(nums_out)
    return nums_out

def to_str(digits):
    return ''.join([str(x) for x in digits])

def compute_day16(input):
    nums_in = [int(x) for x in input.strip()]
    output = apply_fft(nums_in, 100)
    part1 = to_str(output[:8])

    offset = int(input[:7])
    extended_nums_in = nums_in * 10000
    h = len(extended_nums_in)//2
    output_second_half = apply_fft_second_half(extended_nums_in[h:], 100)
    part2_ints = output_second_half[offset-h:offset-h+8]
    part2 = to_str(part2_ints)

    return part1, part2

if __name__ == '__main__':
    with open('day16.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day16(input)
        print(f'part 1: {p1}, part 2: {p2}')
