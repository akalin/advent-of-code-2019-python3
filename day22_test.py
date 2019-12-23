import unittest

from day22 import Shuffle

class TestDay22(unittest.TestCase):
    def test_identity_shuffle(self):
        sh = Shuffle(10)
        cards = list(sh.cards())
        self.assertEqual(cards, list(range(10)))

    def test_cut_shuffle(self):
        sh = Shuffle.cut(10, 3)
        cards = list(sh.cards())
        self.assertEqual(cards, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

        sh = Shuffle.cut(10, -4)
        cards = list(sh.cards())
        self.assertEqual(cards, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()
