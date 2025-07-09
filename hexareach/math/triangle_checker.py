"""
triangle_checker.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import numpy as np


class TriangleChecker:
    """
    三角形が成立するかどうかを判定するクラス.
    """

    def __init__(self) -> None:
        pass

    def check(self, len1: float, len2: float, len3: float) -> bool:
        """
        3辺の長さから三角形が成立するかどうかを判定する関数.
        三角形が成立する場合はTrueを返す.
        a, b, cについて
        (a + b > c) かつ
        (b + c > a) かつ
        (c + a > b)
        が成り立つとき、三角形が成立する.

        パラメータ
        ----------
        len1 : float
            辺1の長さ
        len2 : float
            辺2の長さ
        len3 : float
            辺3の長さ
        """
        # いずれかの2辺の和が残りの1辺以下なら三角形は成立しない.
        if np.abs(len1) + np.abs(len2) <= np.abs(len3):
            return False
        if np.abs(len2) + np.abs(len3) <= np.abs(len1):
            return False
        if np.abs(len3) + np.abs(len1) <= np.abs(len2):
            return False
        return True
