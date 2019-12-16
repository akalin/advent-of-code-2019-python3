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
#        print(i, n, [n] * (i + 1))
        pattern += [n] * (i + 1)
        pi = (pi + 1) % len(base_pattern)
    return pattern[1:num_count+1]

def compute_ith(nums_in, i):
    pattern = get_pattern(len(nums_in), i)
#    print(len(nums_in), len(pattern))
    s = sum([a * b for a, b in zip(nums_in, pattern)])
    s = abs(s) % 10
#    print('convolve', list(zip(nums_in, pattern)), s)
    return s

def do_round(nums_in):
    nums_out = [compute_ith(nums_in, i) for i in range(len(nums_in))]
#    print(nums_in, nums_out)
    return nums_out

def apply_fft(nums_in, rounds):
    nums_out = nums_in
    for i in range(rounds):
        nums_out = do_round(nums_out)
#        print(nums_out)
    return nums_out

def compute_ith_second_half(nums_in, i):
    s = sum(nums_in[i:]) % 10
    return s

def do_round_second_half(nums_in):
    nums_out = [compute_ith_second_half(nums_in, i) for i in range(len(nums_in))]
#    print(nums_in, nums_out)
    return nums_out

def apply_fft_second_half(nums_in, rounds):
    nums_out = nums_in
    for i in range(rounds):
        nums_out = do_round_second_half(nums_out)
    return nums_out

def to_str(digits):
    return ''.join([str(x) for x in digits])

def compute_day16(input):
#    input = '12345678'
    input = '80871224585914546619083218645595'

    nums_in = [int(x) for x in input.strip()]
    output = apply_fft(nums_in, 100)
    part1 = to_str(output[:8])

    h = len(nums_in)//2
    output_second_half = apply_fft_second_half(nums_in[h:], 100)
    if output_second_half != output[h:]:
        raise

    return part1, to_str(output_second_half)

if __name__ == '__main__':
    with open('day16.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day16(input)
        print(f'part 1: {p1}, part 2: {p2}')
