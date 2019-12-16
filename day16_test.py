import unittest

from day16 import parse_input, to_str, apply_fft, extract_message, T_k, T_k_fast

class TestDay16(unittest.TestCase):
    def test_fft_short(self):
        nums_in = parse_input('12345678')
        nums_out = apply_fft(nums_in, 4)
        self.assertEqual(to_str(nums_out), '01029498')

    def test_fft(self):
        test_cases = [
            ('80871224585914546619083218645595', '24176176'),
            ('19617804207202209144916044189917', '73745418'),
            ('69317163492948606335995924319873', '52432133'),
        ]
        for input, expected_out in test_cases:
            nums_in = parse_input(input)
            nums_out = apply_fft(nums_in, 100)
            self.assertEqual(to_str(nums_out[:8]), expected_out)

    def test_T_k_fast(self):
        expected_out = T_k(10, 3, 5)
        out = T_k_fast(10, 3, 5)
        self.assertEqual(out, expected_out)

    def test_extract_message(self):
        test_cases = [
            ('03036732577212944063491565474664', '84462026'),
            ('02935109699940807407585447034323', '78725270'),
            ('03081770884921959731165446850517', '53553731'),
        ]
        for input, expected_out in test_cases:
            msg = extract_message(input)
            self.assertEqual(msg, expected_out)

if __name__ == '__main__':
    unittest.main()
