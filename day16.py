from util import *

def parse_input(input):
    return [int(x) for x in input.strip()]

def to_str(digits):
    return ''.join([str(x) for x in digits])

base_pattern = [0, 1, 0, -1]

def get_pattern(num_count, i):
    pattern = []
    pi = 0
    while len(pattern) < num_count+1:
        n = base_pattern[pi]
        pattern += [n] * (i + 1)
        pi = (pi + 1) % len(base_pattern)
    return pattern[1:num_count+1]

def apply_fft(nums, rounds):
    nums = nums[:]
    c = len(nums)
    for _ in range(rounds):
        for i in range(c):
            s = 0
            sign = 1
            for j in range(i, c, 2 * (i + 1)):
                s += sign * sum(nums[j:j+i+1])
                sign = -sign
            nums[i] = abs(s) % 10
    return nums

# We want to compute A^count where
#
#     [ 1 1 ... 1 1 ]
#     [ 0 1 ... 1 1 ]
# A = [ ...     ... ]
#     [ 0 0 ... 1 1 ]
#     [ 0 0 ... 0 1 ]
#
# i.e. where A has 1s on and above the diagonal.
#
# If you compute A^2, you notice that it looks like
#
#       [ 1 2 ... n-1   n ]
#       [ 0 1 ... n-2 n-1 ]
# A^2 = [ ... ... ... ... ]
#       [ 0 0 ...   1   2 ]
#       [ 0 0 ...   0   1 ]
#
# i.e., each row is the row above shifted 1 to the right, and the entries
# in the first row are the sum of the columns of A. Similarly, the rows of
# A^3 are shifts of the first row, and the first row are the sums of the
# columns of A^2, namely the sums of the first n integers. Therefore, the
# first row of A^3 are the triangular numbers:
#
#       [ 1 3 6 10  ... ]
#       [ 0 1 3  6  ... ]
# A^3 = [       ...     ]
#       [ 0 0 0 ... 1 3 ]
#       [ 0 0 0 ... 0 1 ]
#
# The formula for the nth triangular number is:
#
#   T_{n,3} = B(n+1, 2) = n*(n+1)/2,
#
# where B(n, k) = n!/(k!*(n-k)!) are the binomial coefficients.
#
# Similarly, the first row of A^4 are the tetrahedral numbers, which are
# the sum of the first n triangular numbers. The formula for the nth
# tetrahedral number is:
#
#   T_{n,4} = B(n+2, 3) = n*(n+1)*(n+2)/3.
#
# We can then guess that the first row of A^k follows the formula:
#
#   T_{n,k} = B(n+k-2, k-1).
#
# This is in fact true, and we can show this by showing:
#
#  B(n+k-1, k) = ∑_{m=1}^n B(m+k-2, k-1),
#
# which follows from https://en.wikipedia.org/wiki/Hockey-stick_identity .

def binom(n, k):
    return prod([n - i for i in range(k)]) // prod(range(1, k+1))

# Straightforward (but slow) implementation.

def T_k_slow(max_n, k, modulus):
    return [binom(n+k-2, k-1) % modulus for n in range(1, max_n+1)]

# Compute the binomial coefficients using a running product.

def T_k_fast(max_n, k, modulus):
    out = [0] * max_n
    x = 1
    out[0] = 1
    for n in range(2, max_n + 1):
        x *= (n + k - 2)
        x //= (n - 1)
        out[n - 1] = (x % modulus)
    return out

# Use https://en.wikipedia.org/wiki/Lucas%27s_theorem
# to compute binom(n, k) % p efficiently for prime p.

def binom_mod_p(n, k, p):
    prod = 1
    while True:
        n, n_i = divmod(n, p)
        k, k_i = divmod(k, p)
        prod = (prod * binom(n_i, k_i)) % p
        if n == 0 and k == 0:
            break
    return prod

# Finally, use https://en.wikipedia.org/wiki/Chinese_remainder_theorem to
# compute binom(n, k) % 10 in terms of binom(n, k) % 2 and binom(n, k) % 5.
#
# Since (-2)*2 + 1*5 = 1, the CRT says that if n = a_1 mod 2 and n = a_2 mod 5,
# then n = (5*a_1 - 4*a_2) mod 10.
#
# This is actually slower than T_k_fast above for small inputs,
# though. It's only used for
# https://www.reddit.com/r/adventofcode/comments/ebb8w6/2019_day_16_part_three_a_fanfiction_by_askalski/ .

def binom_mod_10(n, k):
    # Compute binom(n, k) % 2 with bitwise operators.
    a1 = int(not (~n & k))
    a2 = binom_mod_p(n, k, 5)
    return (5*a1 - 4*a2) % 10

def T_k_asympt_fastest(max_n, k, m):
    if m != 10:
        raise Exception('unexpected m={m}')
    return [binom_mod_10(n+k-2, k-1) for n in range(1, max_n+1)]

def apply_fft_second_half(nums_in, rounds, c, T_k):
    modulus = 10
    coeffs = T_k(len(nums_in), rounds, modulus)
    return [sum([(x * y) % modulus for x, y in zip(nums_in[i:], coeffs)]) % modulus for i in range(c)]

def extract_message(input, rounds, T_k):
    nums_in = parse_input(input)
    offset = int(input[:7])
    extended_nums_in = nums_in * 10000
    output = apply_fft_second_half(extended_nums_in[offset:], rounds, 8, T_k)
    return to_str(output)

def compute_day16(input):
    nums_in = parse_input(input)
    output_part1 = apply_fft(nums_in, 100)
    part1 = to_str(output_part1[:8])

    part2 = extract_message(input, 100, T_k_fast)
    return part1, part2

if __name__ == '__main__':
    with open('day16.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day16(input)
        print(f'part 1: {p1}, part 2: {p2}')

    with open('day16_part3.input', 'r') as input_file:
        input = input_file.read()
        p3 = extract_message(input, 287029238942, T_k_asympt_fastest)
        print(f'part 3: {p3}')
