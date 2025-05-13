"""
triangle_checker.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import numpy as np


class TriangleChecker:
    def can_make_triangle(self, len1: float, len2: float, len3: float) -> bool:
        """
        与えられた3つの辺の長さから、三角形が成立するかを判定する関数．\n
        三角形が作れるならばTrueを返す．\n
        a, b, cにおいて
        a + b > c かつ
        b + c > a かつ
        c + a > b
        が成り立てば三角形が作れる．

        Parameters
        ----------
        len1 : float
            辺1の長さ.
        len2 : float
            辺2の長さ.
        len3 : float
            辺3の長さ.
        """

        if np.abs(len1) + np.abs(len2) <= np.abs(len3):
            return False

        if np.abs(len2) + np.abs(len3) <= np.abs(len1):
            return False

        if np.abs(len3) + np.abs(len1) <= np.abs(len2):
            return False

        return True


if __name__ == "__main__":
    tc = TriangleChecker()
    print(tc.can_make_triangle(3, 4, 5))  # True
    print(tc.can_make_triangle(3, 4, 7))  # False
