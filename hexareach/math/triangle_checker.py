"""
triangle_checker.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import numpy as np


class TriangleChecker:
    """
    三角形の成立を判定するクラス．
    """
    def __init__(self) -> None:
        pass

    def check(self, len1: float, len2: float, len3: float) -> bool:
        """
        Function to determine if a triangle is formed
        from the lengths of three given sides. \n
        Returns True if the triangle can be formed. \n
        For a, b, c
        (a + b > c) and
        (b + c > a) and
        (c + a > b)
        is true, then a triangle can be formed.

        Parameters
        ----------
        len1 : float
            Length of side 1.
        len2 : float
            Length of side 2.
        len3 : float
            The length of side 3.
        """

        if np.abs(len1) + np.abs(len2) <= np.abs(len3):
            return False

        if np.abs(len2) + np.abs(len3) <= np.abs(len1):
            return False

        if np.abs(len3) + np.abs(len1) <= np.abs(len2):
            return False

        return True
