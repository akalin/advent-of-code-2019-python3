import itertools
from util import *

# A shuffle represents an operation on a deck of cards.
class Shuffle(object):
    def __init__(self, n, a=1, b=0):
        # n is the number of cards, which have numbers 0 to n-1.
        # Given a and b, if x is a list of cards, and y is the
        # list of cards after this shuffle is applied, then
        #
        #   y[i] == x[f(i)]
        #
        # where f(i) = (ai + b) % n. In other words, f permutes the
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
        # permutations on the indices. If f1 and f2 are the respective
        # permutations of self and other, and x is a list of cards, y
        # is the list of cards after self is applied to x, and z is the
        # list of cards after other is applied to y, then
        #
        #   z[i] = y[f2(i)] = x[f1(f2(i))].
        #
        # Letting
        #
        #   f1(i) = ai + b    and    f2(i) = ci + d,
        #
        # we then have
        #
        #   f1(f2(i)) = a(ci + d) + b = (ac)i + (ad + b).
        return Shuffle(self.n, self.a * other.a, self.a * other.b + self.b)

    def inverse(self):
        # Solving
        #
        #  j = ai + b,
        #
        # we have i = j/a - b/a, which also works mod n, assuming a is
        # invertible mod n.
        a_inv = modinv(self.a, self.n)
        return Shuffle(self.n, a_inv, -a_inv * self.b)

    # Returns the cards resulting from this shuffle applied to the
    # factory deck x[i] = i.
    def cards(self):
        for i in range(self.n):
            yield (self.a*i + self.b) % self.n

    def cut(n, N):
        # Given a deck x, the cut deck is defined by
        #
        #   y[i] = x[i + N].
        return Shuffle(n, 1, N)

    def increment(n, N):
        # Given a deck x, the incremented deck is defined by
        #
        #   y[N*i] = x[i].
        #
        # Therefore, y[i] = x[i/N], and thus f(i) = i/N.
        return Shuffle(n, modinv(N, n), 0)

    def new_stack(n):
        # Given a deck x, the new stack is defined by
        #
        #   y[-i] = x[i].
        #
        # Therefore, y[i] = x[-i] = x[n - 1 - i], and thus f(i) = -i - 1.
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
