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
            ('''
            -1,2,2,0
            0,0,2,-2
            0,0,0,-2
            -1,2,0,0
            -2,-2,-2,2
            3,0,2,-1
            -1,3,2,2
            -1,0,-1,0
            0,2,1,-2
            3,0,0,0
            ''', 4),
            ('''
            1,-1,0,1
            2,0,-1,0
            3,2,-1,0
            0,0,3,1
            0,0,-1,-1
            2,3,-2,0
            -2,2,0,0
            2,-2,0,-1
            1,-1,0,-1
            3,2,0,2
            ''', 3),
            ('''
            1,-1,-1,-2
            -2,-2,0,1
            0,2,1,3
            -2,3,-2,1
            0,2,3,-2
            -1,-1,1,-2
            0,-2,-1,0
            -2,2,3,-1
            1,2,2,0
            -1,-2,0,-2
            ''', 8),
        ]
        for input, expected_count in cases:
            points = parse_input(input)
            count = get_constellation_count(points)
            self.assertEqual(count, expected_count)

if __name__ == '__main__':
    unittest.main()
