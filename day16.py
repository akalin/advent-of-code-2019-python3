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
# A^2 = [ ...       ...   ]
#       [ 0 0 ...   1   2 ]
#       [ 0 0 ...   0   1 ]
#
# i.e., each row is the row above shifted 1 to the right, and the entries
# in the first row are the sum of the columns of A. Similarly, the rows of
# A^3 are shifts of the first row, and the first row are the sums of the
# columns of A^2, namely the sums of the first n integers. Therefore, the
# first row of A^3 are the triangular numbers:
#
# A^3 = [ 1 3 6 10 ... ]
#       [ 0 1 3  6 ... ]
#         ...
#
# The formula for the nth triangular number is:
#
#   T_n = B(n+1, 2) = n*(n+1)/2,
#
# where B(n, k) = n!/(k!(n-k)!) are the binomial coefficients.
#
# Similarly, the first row of A^4 are the tetrahedral numbers, which are
# the sum of the first n triangular numbers. The formula for the nth
# tetrahedral number is:
#
#   S_n = B(n+2, 3) = n*(n+1)*(n+2)/3.
#
# We can then guess that the first row of A^k follows the formula:
#
#   R_{n,k} = B(n+k-1, k).
#
# This is in fact true, and we can show this by showing:
#
#  B(n+k-1, k) = ∑_{m=1}^n B(m+k-2, k-1),
#
# which follows from https://en.wikipedia.org/wiki/Hockey-stick_identity .
#
# (We can in fact go further, since we only need the binomial
# coefficients mod 10. To do so we need to apply Lucas' theorem to
# compute the binomial coefficients mod 2 and 5, and then use the
# Chinese remainder theorem to use those to compute the mod 10:
# see https://gist.github.com/alexanderhaupt/1ac31ecbd316aca32c469f42d8646c98 )
#
# Therefore, given max_n and k, we compute R_{n,k}, which is the first
# row of A^k, and then we can apply A^k to our input data.

def binoms(max_n, k, modulus):
    coeffs = [0] * max_n
    x = 1
    coeffs[0] = 1
    for n in range(2, max_n + 1):
        x *= (n + k - 1)
        x //= (n - 1)
        coeffs[n - 1] = (x % modulus)
    return coeffs

def apply_fft_second_half(nums_in, rounds, count):
    coeffs = binoms(len(nums_in), rounds - 1, 10)
    nums_out = [0] * count
    for i in range(count):
        nums_out[i] = sum([(x * y) % 10 for x, y in zip(nums_in[i:], coeffs)]) % 10
    return nums_out

def compute_day16(input):
    nums_in = parse_input(input)
    output = apply_fft(nums_in, 100)
    part1 = to_str(output[:8])

    offset = int(input[:7])
    extended_nums_in = nums_in * 10000

    dim = len(extended_nums_in) - offset

    output_second_half = apply_fft_second_half(extended_nums_in[offset:], 100, 8)
    part2 = to_str(output_second_half)

    return part1, part2

if __name__ == '__main__':
    with open('day16.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day16(input)
        print(f'part 1: {p1}, part 2: {p2}')
