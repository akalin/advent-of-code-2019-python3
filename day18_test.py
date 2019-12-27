import unittest

from day18 import parse_map, compute_shortest_steps

class TestDay18(unittest.TestCase):
    def test_compute_shortest_steps(self):
        cases = [
            ('''
            #########
            #b.A.@.a#
            #########
            ''', 1, 8),
            ('''
            ########################
            #f.D.E.e.C.b.A.@.a.B.c.#
            ######################.#
            #d.....................#
            ########################
            ''', 1, 86),
            ('''
            #################
            #i.G..c...e..H.p#
            ########.########
            #j.A..b...f..D.o#
            ########@########
            #k.E..a...g..B.n#
            ########.########
            #l.F..d...h..C.m#
            #################
            ''', 1, 136),
            ('''
            ########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################
            ''', 1, 81),
            ('''
            #######
            #a.#Cd#
            ##@#@##
            #######
            ##@#@##
            #cB#Ab#
            #######
            ''', 4, 8),
            ('''
            ###############
            #d.ABC.#.....a#
            ######@#@######
            ###############
            ######@#@######
            #b.....#.....c#
            ###############
            ''', 4, 24),
            ('''
            #############
            #DcBa.#.GhKl#
            #.###@#@#I###
            #e#d#####j#k#
            ###C#@#@###J#
            #fEbA.#.FgHi#
            #############
            ''', 4, 32),
            ('''
            #############
            #g#f.D#..h#l#
            #F###e#E###.#
            #dCba@#@BcIJ#
            #############
            #nK.L@#@G...#
            #M###N#H###.#
            #o#m..#i#jk.#
            #############
            ''', 4, 72),
        ]
        for input, start_count, expected_shortest_steps in cases:
            args = parse_map(input, start_count)
            shortest_steps = compute_shortest_steps(*args)
            self.assertEqual(shortest_steps, expected_shortest_steps)

if __name__ == '__main__':
    unittest.main()
