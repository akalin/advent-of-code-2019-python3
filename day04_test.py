import unittest

from day04 import can_be_password

class TestDay04(unittest.TestCase):
    def test_can_be_password(self):
        self.assertEqual(can_be_password(111111), (True, False))
        self.assertEqual(can_be_password(223450), (False, False))
        self.assertEqual(can_be_password(123789), (False, False))
        self.assertEqual(can_be_password(112233), (True, True))
        self.assertEqual(can_be_password(123444), (True, False))
        self.assertEqual(can_be_password(111122), (True, True))

if __name__ == '__main__':
    unittest.main()
