"""
circle_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from matplotlib.axes import Axes
from matplotlib.patches import Circle

class CircleRenderer:
    """
    円を描画するクラス。
    このクラスは指定された半径と中心座標を用いて円を描画する。
    """

    def __init__(
            self,
            ax: Axes,
            radius: float,
            center: tuple[float, float],
            color: str,
            alpha: float) -> None:
        self._ax = ax

        self._circle = Circle(center, color=color, fill=False)
        self._circle.set_radius(radius)
        self._circle.set_alpha(alpha)


    def render(self) -> None:
        """
        円を描画するメソッド.
        """
        self._ax.add_artist(self._circle)

    def update_center(self, center: tuple[float, float]) -> None:
        """
        円の中心座標を更新するメソッド.

        Parameters
        ----------
        center : tuple[float, float]
            新しい中心座標 (x, y)
        """
        self._circle.center = center
