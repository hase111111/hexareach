"""
wedge_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from matplotlib.axes import Axes
from matplotlib import patches as patch

class WedgeRenderer:
    """
    扇形を描画するクラス.
    """

    def __init__(
            self,
            ax: Axes,
            radius: float,
            center: tuple[float, float],
            color: str,
            alpha: float) -> None:
        self._ax = ax

        self._wedge = patch.Wedge(center, radius, 0, 10)
        self._wedge.set_radius(radius)
        self._wedge.set_alpha(alpha)
        self._wedge.set_facecolor(color)


    def render(self) -> None:
        """
        円を描画するメソッド.
        """
        self._ax.add_patch(self._wedge)

    def update(self, center: tuple[float, float], theta1: float, theta2: float) -> None:
        """
        円の中心座標を更新するメソッド.

        Parameters
        ----------
        center : tuple[float, float]
            新しい中心座標 (x, y)
        """
        self._wedge.set_center(center)
        self._wedge.set_theta1(theta1)
        self._wedge.set_theta2(theta2)
