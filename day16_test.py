import unittest

from day16 import parse_input, to_str, apply_fft, extract_message, T_k_slow, T_k_fast, T_k_asympt_fastest, binom, binom_mod_p, binom_mod_10

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
        n = 10
        k = 3
        m = 5
        expected_out = T_k_slow(n, k, m)
        out = T_k_fast(n, k, m)
        self.assertEqual(out, expected_out)

    def test_T_k_asympt_fastest(self):
        n = 10
        k = 3
        m = 10
        expected_out = T_k_slow(n, k, m)
        out = T_k_asympt_fastest(n, k, m)
        self.assertEqual(out, expected_out)

    def test_binom_mod_p(self):
        n = 10
        k = 3
        m = 5
        expected_out = binom(n, k) % m
        out = binom_mod_p(n, k, m)
        self.assertEqual(out, expected_out)

    def test_binom_mod_10(self):
        n = 9
        k = 7
        expected_out = binom(n, k) % 10
        out = binom_mod_10(n, k)
        self.assertEqual(out, expected_out)

    def test_extract_message(self):
        test_cases = [
            ('03036732577212944063491565474664', '84462026'),
            ('02935109699940807407585447034323', '78725270'),
            ('03081770884921959731165446850517', '53553731'),
        ]
        for T_k in [T_k_slow, T_k_fast, T_k_asympt_fastest]:
            for input, expected_out in test_cases:
                msg = extract_message(input, 100, T_k)
                self.assertEqual(msg, expected_out)

if __name__ == '__main__':
    unittest.main()
