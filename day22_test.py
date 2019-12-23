import unittest

from day22 import Shuffle

class TestDay22(unittest.TestCase):
    def test_identity_shuffle(self):
        sh = Shuffle(10)
        cards = list(sh.cards())
        self.assertEqual(cards, list(range(10)))

    def test_cut(self):
        sh = Shuffle.cut(10, 3)
        cards = list(sh.cards())
        self.assertEqual(cards, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

        sh = Shuffle.cut(10, -4)
        cards = list(sh.cards())
        self.assertEqual(cards, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

    def test_increment(self):
        sh = Shuffle.increment(10, 3)
        cards = list(sh.cards())
        self.assertEqual(cards, [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

    def test_new_stack(self):
        sh = Shuffle.new_stack(10)
        cards = list(sh.cards())
        self.assertEqual(cards, list(range(9, -1, -1)))

    n = 10
    cases = [
        ('''
        deal with increment 7
        deal into new stack
        deal into new stack
        ''',
         Shuffle.new_stack(n) *
         Shuffle.new_stack(n) *
         Shuffle.increment(n, 7),
         [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
        ('''
        cut 6
        deal with increment 7
        ''',
         Shuffle.increment(n, 7) *
         Shuffle.cut(n, 6),
         [6, 9, 2, 5, 8, 1, 4, 7, 0, 3]),
        ('''
        cut 6
        deal with increment 7
        deal into new stack
        ''',
         Shuffle.new_stack(n) *
         Shuffle.increment(n, 7) *
         Shuffle.cut(n, 6),
         [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]),
        ('''
        deal with increment 7
        deal with increment 9
        cut -2
        ''',
         Shuffle.cut(n, -2) *
         Shuffle.increment(n, 7) *
         Shuffle.increment(n, 9),
         [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]),
        ('''
        deal into new stack
        cut -2
        deal with increment 7
        cut 8
        cut -4
        deal with increment 7
        cut 3
        deal with increment 9
        deal with increment 3
        cut -1
        ''',
         Shuffle.cut(n, -1) *
         Shuffle.increment(n, 3) *
         Shuffle.increment(n, 9) *
         Shuffle.cut(n, 3) *
         Shuffle.increment(n, 7) *
         Shuffle.cut(n, -4) *
         Shuffle.cut(n, 8) *
         Shuffle.increment(n, 7) *
         Shuffle.cut(n, -2) *
         Shuffle.new_stack(n),
         [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]),
    ]

    def test_mult(self):
        for _, sh, expected_cards in self.__class__.cases:
            cards = list(sh.cards())
            self.assertEqual(cards, expected_cards, f'sh is {sh}')

    def test_parse(self):
        for input, expected_sh, _ in self.__class__.cases:
            sh = Shuffle.parse_multiple(self.__class__.n, input)
            self.assertEqual(sh, expected_sh, f'input is {input}')

if __name__ == '__main__':
    unittest.main()
