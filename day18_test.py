import unittest

from day18 import compute_shortest_steps

class TestDay18(unittest.TestCase):
    def test_compute_shortest_steps(self):
        cases = [
            ('''
            #########
            #b.A.@.a#
            #########
            ''', 8),
            ('''
            ########################
            #f.D.E.e.C.b.A.@.a.B.c.#
            ######################.#
            #d.....................#
            ########################
            ''', 86),
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
            ''', 136),
            ('''
            ########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################
            ''', 81),
        ]
        for input, expected_shortest_steps in cases:
            shortest_steps = compute_shortest_steps(input)
            self.assertEqual(shortest_steps, expected_shortest_steps)

if __name__ == '__main__':
    unittest.main()
