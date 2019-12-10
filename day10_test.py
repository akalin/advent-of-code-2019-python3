import unittest

from day10 import parse_asteroids, compute_best_location

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
             ''', (5, 8), 33),
            ('''
            #.#...#.#.
            .###....#.
            .#....#...
            ##.#.#.#.#
            ....#.#.#.
            .##..###.#
            ..#...##..
            ..##....##
            ......#...
            .####.###.
             ''', (1, 2), 35),
            ('''
            .#..#..###
            ####.###.#
            ....###.#.
            ..###.##.#
            ##.##.#.#.
            ....###..#
            ..#.#..#.#
            #..#.#.###
            .##...##.#
            .....#.#..
             ''', (6, 3), 41),
            ('''
            .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##
             ''', (11, 13), 210),
        ]

        for input, expected_best_location, expected_detected_count in examples:
            asteroids = parse_asteroids(input)
            best_location, detected_count = compute_best_location(asteroids)
            self.assertEqual(best_location, expected_best_location)
            self.assertEqual(detected_count, expected_detected_count)

if __name__ == '__main__':
    unittest.main()
