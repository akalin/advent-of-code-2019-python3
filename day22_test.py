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

    def test_mult(self):
        n = 10
        sh = (Shuffle.increment(n, 7) *
              Shuffle.new_stack(n) *
              Shuffle.new_stack(n))
        cards = list(sh.cards())
        self.assertEqual(cards, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

        sh = (Shuffle.cut(n, 6) *
              Shuffle.increment(n, 7) *
              Shuffle.new_stack(n))
        cards = list(sh.cards())
        self.assertEqual(cards, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])

        sh = (Shuffle.increment(n, 7) *
              Shuffle.increment(n, 9) *
              Shuffle.cut(n, -2))
        cards = list(sh.cards())
        self.assertEqual(cards, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])

        sh = (Shuffle.new_stack(n) *
              Shuffle.cut(n, -2) *
              Shuffle.increment(n, 7) *
              Shuffle.cut(n, 8) *
              Shuffle.cut(n, -4) *
              Shuffle.increment(n, 7) *
              Shuffle.cut(n, 3) *
              Shuffle.increment(n, 9) *
              Shuffle.increment(n, 3) *
              Shuffle.cut(n, -1))
        cards = list(sh.cards())
        self.assertEqual(cards, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

if __name__ == '__main__':
    unittest.main()
