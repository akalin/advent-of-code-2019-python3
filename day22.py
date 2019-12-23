import itertools
from util import *

# A shuffle represents an operation on a deck of cards.
class Shuffle(object):
    def __init__(self, n, a=1, b=0):
        # n is the number of cards, which have numbers 0 to n-1.
        # Given a and b, if a deck looks like
        #
        #   x_0 x_1 ... x_n,
        #
        # then the deck after this shuffle is applied looks like
        #
        #   x_{f(0)} x_{f(1)} ... x_{f(n)}
        #
        # where f(x) = (ax + b) % n. In other words, f permutes the
        # indices of the cards of the deck.
        self.n = n
        self.a = a % n
        self.b = b % n

    def __repr__(self):
        return f'Shuffle(n={self.n}, a={self.a}, b={self.b})'

    def __eq__(self, other):
        return self.n == other.n and self.a == other.a and self.b == other.b

    def __mul__(self, other):
        if self.n != other.n:
            raise Exception(f'{self} and {other} have different values of n')
        # Multiplication is defined as function application _on the right_,
        # meaning that self * other means applying self to a deck first,
        # then applying other to the resulting deck.
        #
        # This is to match the behavior of the corresponding
        # permutations. If f1 and f2 are the permutations of
        # indices, then if a deck looks like
        #
        #   x_0 x_1 ... x_n,
        #
        # and the deck after self is applied looks like
        #
        #   y_0 y_1 ... y_n
        #
        # such that y_k = x_{f1(k)}, then the deck after other is applied
        # looks like
        #
        #   y_{f2(0)} y_{f2(1)} ... y{f2(n)},
        #
        # which, substituting in y_k above, looks like
        #
        #   x_{f1(f2(0))} x_{f1(f2(1))} ... x{f1(f2(n))}.
        #
        # Letting
        #
        #   f1 = ax + b    and    f2 = cx + d,
        #
        # we then have
        #
        #   f1 . f2 = a(cx + d) + b = (ac)x + (ad + b)
        return Shuffle(self.n, self.a * other.a, self.a * other.b + self.b)

    def inverse(self):
        # Solving
        #
        #  y = ax + b,
        #
        # we have x = y/a - b/a, which also works mod n, assuming a is
        # invertible mod n.
        a_inv = modinv(self.a, self.n)
        return Shuffle(self.n, a_inv, -a_inv * self.b)

    # Returns the cards resulting from this shuffle applied to the
    # factory deck 0 1 2 ... n-1.
    def cards(self):
        for i in range(self.n):
            yield (self.a*i + self.b) % self.n

    def cut(n, N):
        return Shuffle(n, 1, N)

    def increment(n, N):
        # x_0 is fixed which means b=0, and x_1 is moved to index N,
        # which means f(N) = a*N = 1, so a is the inverse of N mod n.
        return Shuffle(n, modinv(N, n), 0)

    def new_stack(n):
        return Shuffle(n, -1, -1)

    def parse(n, line):
        if line.find('\n') != -1:
            raise Exception(f'parse called with multiple lines "{line}"')
        words = line.strip().split(' ')
        if words[0] == 'cut':
            N = int(words[1])
            return Shuffle.cut(n, N)
        elif words[0] == 'deal' and words[1] == 'with':
            N = int(words[3])
            return Shuffle.increment(n, N)
        elif words[0] == 'deal' and words[1] == 'into':
            return Shuffle.new_stack(n)
        raise Exception(f'could not parse line "{line}"')

    def parse_multiple(n, input):
        shuffles = [Shuffle.parse(n, line) for line in input.strip().split('\n')]
        return prod(shuffles, Shuffle(n))

def compute_day22(input):
    n1 = 10007
    sh1 = Shuffle.parse_multiple(n1, input)
    sh1_inv = sh1.inverse()
    part1 = next(itertools.islice(sh1_inv.cards(), 2019, None))

    n2 = 119315717514047
    sh2 = Shuffle.parse_multiple(n2, input)
    sh2_rep = fastpow(sh2, 101741582076661, Shuffle(n2))
    part2 = next(itertools.islice(sh2_rep.cards(), 2020, None))

    return part1, part2

if __name__ == '__main__':
    with open('day22.input', 'r') as input_file:
        input = input_file.read()
        part1, part2 = compute_day22(input)
        print(f'part1: {part1}, part2: {part2}')
