import itertools
from util import *

# A shuffle represents an operation on a deck of cards.
class Shuffle(object):
    def __init__(self, n, a=1, b=0):
        # n is the number of cards, which have numbers 0 to n-1.
        # Given a and b, if the cards 0, 1, ... n-1 are the standard deck,
        # then the deck after this shuffle is applied looks like
        #
        #   f(0) f(1) ... f(n - 1)
        #
        # where f(x) = (ax + b) % n.
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
        # self * other is composition, meaning that other is applied first,
        # then self. If self is represented by f(x), ans other is represented
        # by g(x), then other applied to the standard deck looks like
        #
        #   D1 = g(0) g(1) ... g(n - 1),
        #
        # so if self applied to the standard deck looks like
        #
        #   f(0) f(1) ... f(n - 1),
        #
        # then for example if f(0) = 3, then self applied to D1 puts
        # the fourth card of D1 first, i.e. the first card of self applied
        # to D1 is g(3) = g(f(0)). Similarly, self applied to D1 looks like
        #
        #   g(f(0)) g(f(1)) ... g(f(n - 1)),
        #
        # i.e. the representing functions compose in the opposite way
        # than the shuffles do.
        #
        # therefore, if f(x) = ax + b and g(x) = cx + d, then
        # the representing function of self * other is
        #
        #   g(f(x)) = c(ax + b) + d = (ca)x + (cb + d).
        return Shuffle(self.n, other.a * self.a, other.a * self.b + other.b)

    def inverse(self):
        a_inv = modinv(self.a, self.n)
        return Shuffle(self.n, a_inv, -a_inv * self.b)

    def cards(self):
        for i in range(self.n):
            yield (self.a*i + self.b) % self.n

    def cut(n, N):
        return Shuffle(n, 1, N)

    def increment(n, N):
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
        return prod(reversed(shuffles), Shuffle(n))

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
