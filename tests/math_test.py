"""
test_math_util.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import unittest
from hexareach.math.triangle_checker import TriangleChecker


class TestTriangleChecker(unittest.TestCase):
    """
    Test cases for the TriangleChecker class.
    """

    def setUp(self):
        self.triangle_checker = TriangleChecker()

    def test_can_make_triangle(self):
        """
        Test if the triangle can be formed with given lengths.
        """

        self.assertTrue(self.triangle_checker.check(3, 4, 5))
        self.assertTrue(self.triangle_checker.check(3, 5, 4))
        self.assertTrue(self.triangle_checker.check(4, 3, 5))
        self.assertTrue(self.triangle_checker.check(4, 5, 3))
        self.assertTrue(self.triangle_checker.check(5, 3, 4))
        self.assertTrue(self.triangle_checker.check(5, 4, 3))

        self.assertFalse(self.triangle_checker.check(1, 1, 2))
        self.assertFalse(self.triangle_checker.check(1, 2, 1))
        self.assertFalse(self.triangle_checker.check(2, 1, 1))


if __name__ == "__main__":
    unittest.main()
