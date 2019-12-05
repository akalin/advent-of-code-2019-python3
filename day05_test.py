import unittest

from day05 import run_prog

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

if __name__ == '__main__':
    unittest.main()
