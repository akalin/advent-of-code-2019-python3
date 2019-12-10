import unittest

from day10 import parse_asteroids, compute_best_location, vaporize_asteroids

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

    def test_part2_small(self):
        input = '''
        .#....#####...#..
        ##...##.#####..##
        ##...#...#.#####.
        ..#.....X...###..
        ..#.#.....#....##
        '''

        asteroids = parse_asteroids(input)

        expected_vaporized_asteroids = [
            (8, 1),
            (9, 0),
            (9, 1),
            (10, 0),
            (9, 2),
            (11, 1),
            (12, 1),
            (11, 2),
            (15, 1),
            (12, 2),
            (13, 2),
            (14, 2),
            (15, 2),
            (12, 3),
            (16, 4),
            (15, 4),
            (10, 4),
            (4, 4),
            (2, 4),
            (2, 3),
            (0, 2),
            (1, 2),
            (0, 1),
            (1, 1),
            (5, 2),
            (1, 0),
            (5, 1),
            (6, 1),
            (6, 0),
            (7, 0),
            (8, 0),
            (10, 1),
            (14, 0),
            (16, 1),
            (13, 3),
            (14, 3),
        ]

        angles = list(vaporize_asteroids(asteroids, (8, 3)))
        vaporized_asteroids = [p for p, _ in angles]
        self.assertEqual(vaporized_asteroids, expected_vaporized_asteroids)

    def test_part2_big(self):
        input = '''
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
        '''

        asteroids = parse_asteroids(input)

        angles = list(vaporize_asteroids(asteroids, (11, 13)))
        asteroids = [p for p, _ in angles]
        self.assertEqual(asteroids[:3], [(11, 12), (12, 1), (12, 2)])
        self.assertEqual(asteroids[9], (12, 8))
        self.assertEqual(asteroids[19], (16, 0))
        self.assertEqual(asteroids[49], (16, 9))
        self.assertEqual(asteroids[99], (10, 16))
        self.assertEqual(asteroids[198], (9, 6))
        self.assertEqual(asteroids[199], (8, 2))
        self.assertEqual(asteroids[200], (10, 9))
        self.assertEqual(asteroids[298], (11, 1))

if __name__ == '__main__':
    unittest.main()
