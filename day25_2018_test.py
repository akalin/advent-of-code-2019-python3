import unittest

from day25_2018 import parse_input, get_constellation_count

class TestDay25_2018(unittest.TestCase):
    def test_get_constellation_count(self):
        cases = [
            ('''
            0,0,0,0
            3,0,0,0
            0,3,0,0
            0,0,3,0
            0,0,0,3
            0,0,0,6
            9,0,0,0
            12,0,0,0
            ''', 2),
        ]
        for input, expected_count in cases:
            points = parse_input(input)
            count = get_constellation_count(points)
            self.assertEqual(count, expected_count)

if __name__ == '__main__':
    unittest.main()
