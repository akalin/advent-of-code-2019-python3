import unittest

from day06 import count_orbits, count_transfers, count_orbits_nx, count_transfers_nx

class TestDay06(unittest.TestCase):
    def test_count_orbits(self):
        input = '''
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        '''

        num_orbits = count_orbits(input)
        self.assertEqual(num_orbits, 42)

        num_orbits = count_orbits_nx(input)
        self.assertEqual(num_orbits, 42)

    def test_count_transfers(self):
        input = '''
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        K)YOU
        I)SAN
        '''

        num_orbits = count_transfers(input)
        self.assertEqual(num_orbits, 4)

        num_orbits = count_transfers_nx(input)
        self.assertEqual(num_orbits, 4)

if __name__ == '__main__':
    unittest.main()
