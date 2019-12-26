import unittest

from day18 import compute_shortest_steps

class TestDay18(unittest.TestCase):
    def test_get_constellation_count(self):
        cases = [
            ('''
            #########
            #b.A.@.a#
            #########
            ''', 8),
        ]
        for input, expected_shortest_steps in cases:
            shortest_steps = compute_shortest_steps(input)
            self.assertEqual(shortest_steps, expected_shortest_steps)

if __name__ == '__main__':
    unittest.main()
