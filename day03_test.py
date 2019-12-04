import unittest

from day03 import compute_closest_intersection

test_cases = [
    ('''
    R8,U5,L5,D3
    U7,R6,D4,L4
    ''', 6, 30),
    ('''
    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83
    ''', 159, 610),
    ('''
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
    ''', 135, 410),
]

class TestDay03(unittest.TestCase):
    def test(self):
        for input, expected_min_manhattan_distance, expected_min_step_count in test_cases:
            min_manhattan_distance, min_step_count = compute_closest_intersection(input)
            self.assertEqual(min_manhattan_distance, expected_min_manhattan_distance)
            self.assertEqual(min_step_count, expected_min_step_count)

if __name__ == '__main__':
    unittest.main()
