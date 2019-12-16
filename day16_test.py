import unittest

from day16 import parse_input, to_str, apply_fft

class TestDay16(unittest.TestCase):
    def test_fft_short(self):
        nums_in = parse_input('12345678')
        nums_out = apply_fft(nums_in, 4)
        self.assertEqual(to_str(nums_out), '01029498')

if __name__ == '__main__':
    unittest.main()
