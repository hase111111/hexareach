"""
test_math_util.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import unittest
import phantom_cross as pc


class TestTriangleChecker(unittest.TestCase):
    def setUp(self):
        self.triangle_checker = pc.TriangleChecker()

    def test_can_make_triangle(self):
        self.assertTrue(self.triangle_checker.can_make_triangle(3, 4, 5))
        self.assertTrue(self.triangle_checker.can_make_triangle(3, 5, 4))
        self.assertTrue(self.triangle_checker.can_make_triangle(4, 3, 5))
        self.assertTrue(self.triangle_checker.can_make_triangle(4, 5, 3))
        self.assertTrue(self.triangle_checker.can_make_triangle(5, 3, 4))
        self.assertTrue(self.triangle_checker.can_make_triangle(5, 4, 3))

        self.assertFalse(self.triangle_checker.can_make_triangle(1, 1, 2))
        self.assertFalse(self.triangle_checker.can_make_triangle(1, 2, 1))
        self.assertFalse(self.triangle_checker.can_make_triangle(2, 1, 1))


if __name__ == "__main__":
    unittest.main()
