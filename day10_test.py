import unittest

from day10 import compute_best_asteroid

class TestDay10(unittest.TestCase):
    def test_part1(self):
        examples = [
            ('''
            ......#.#.
            #..#.#....
            ..#######.
            .#.#.###..
            .#..#.....
            ..#....#.#
            #..#....#.
            .##.#..###
            ##...#..#.
            .#....####
             ''', (5, 8), 33)
        ]

        for map, expected_best_asteroid, expected_visible_count in examples:
            best_asteroid, visible_count = compute_best_asteroid(map)
            self.assertEqual(best_asteroid, expected_best_asteroid)
            self.assertEqual(visible_count, expected_visible_count)

if __name__ == '__main__':
    unittest.main()
