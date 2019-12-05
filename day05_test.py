import unittest

from day05 import run_prog
from itertools import chain

class TestDay04(unittest.TestCase):
    def test_io(self):
        for x in range(-100, 100):
            _, output = run_prog([3,0,4,0,99], [x])
            self.assertEqual(output, [x])

    def test_immediate(self):
        memory, _ = run_prog([1002,4,3,4,33], [])
        self.assertEqual(memory, [1002,4,3,4,99])

    def test_negative(self):
        memory, _ = run_prog([1101,100,-1,4,0], [])
        self.assertEqual(memory, [1101,100,-1,4,99])

    def test_eq8_pos(self):
        prog = [3,9,8,9,10,9,4,9,99,-1,8]

        _, output = run_prog(prog, [8])
        self.assertEqual(output, [1])

        for x in chain(range(-100, 8), range(9, 100)):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [0])

    def test_le8_pos(self):
        prog = [3,9,7,9,10,9,4,9,99,-1,8]

        for x in range(-100, 8):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [1])

        for x in range(8, 100):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [0])

    def test_eq8_imm(self):
        prog = [3,3,1108,-1,8,3,4,3,99]

        _, output = run_prog(prog, [8])
        self.assertEqual(output, [1])

        for x in chain(range(-100, 8), range(9, 100)):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [0])

    def test_le8_imm(self):
        prog = [3,3,1107,-1,8,3,4,3,99]

        for x in range(-100, 8):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [1])

        for x in range(8, 100):
            _, output = run_prog(prog, [x])
            self.assertEqual(output, [0])

if __name__ == '__main__':
    unittest.main()
