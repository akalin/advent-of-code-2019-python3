import unittest

from day07 import run_prog_series2

class TestDay06(unittest.TestCase):
    def test_part02(self):
        program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        output = run_prog_series2(program, [9,8,7,6,5])
        self.assertEqual(output, 139629729)

        program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        output = run_prog_series2(program, [9,7,8,5,6])
        self.assertEqual(output, 18216)

if __name__ == '__main__':
    unittest.main()
