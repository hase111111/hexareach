"""
approximated_graph_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import matplotlib.axes as axes
import numpy as np

from ..hexapod_leg_range_calculator import HexapodLegRangeCalculator


class ApproximatedGraphRenderer:

    def __init__(
        self,
        hexapod_leg_range_calc: HexapodLegRangeCalculator,
        ax: axes.Axes,
        z_min: float = -300,
        z_max: float = 300,
        draw_additional_line: bool = True,
        draw_fill: bool = True,
        color: str = "green",
        alpha: float = 1.0,
    ) -> None:
        self._calc = hexapod_leg_range_calc
        self._ax = ax
        self._GRAPH_STEP = 0.01

        if self._calc is None:
            raise ValueError("calc_instance is None")

        if self._ax is None:
            raise ValueError("ax is None")

        self.set_draw_additional_line(draw_additional_line)
        self.set_draw_fill(draw_fill)
        self.set_color(color)
        self.set_alpha(alpha)
        self.set_range(z_min, z_max)

    def render(self) -> None:
        """
        近似された(Approximated)脚可動範囲の表示を行う．
        セット関数はこの関数の前に呼び出す必要がある．
        """

        print("ApproximatedGraphRenderer.render: Shows approximate leg range of motion")
        print(
            "ApproximatedGraphRenderer.render: "
            + "z_min = "
            + str(self._z_min)
            + "[mm], "
            + "z_max = "
            + str(self._z_max)
            + "[mm], "
            + "draw_additional_line = "
            + str(self._draw_additional_line)
            + ", "
            + "color = "
            + self._color
            + ", "
            + "alpha = "
            + str(self._alpha)
            + ", "
            + "draw_fill = "
            + str(self._draw_fill)
            + ", "
            + "(step = "
            + str(self._GRAPH_STEP)
            + ")"
        )

        # 近似された(Approximated)脚可動範囲の計算を行う．
        # GRAPH_STEP刻みでZ_MINからZ_MAXまでの配列zを作成．
        z = np.arange(self._z_min, self._z_max, self._GRAPH_STEP)

        # xと同じ要素数で値がすべて min_leg_radius の配列zを作成．
        approximated_x_min = np.full_like(
            z, self._calc.get_approximate_min_leg_raudus()
        )

        approximated_x_max = []
        for i in range(len(z)):
            approximated_x_max.append(self._calc.get_approximate_max_leg_raudus(z[i]))

        if self._draw_additional_line:
            # 補助線を描画する．
            self._ax.plot(approximated_x_min, z, color=self._color, alpha=0.1)
            self._ax.plot(approximated_x_max, z, color=self._color, alpha=0.1)

        # xとzで囲まれた範囲をfillする．
        if self._draw_fill:
            self._ax.fill_betweenx(
                z,
                approximated_x_min,
                approximated_x_max,
                where=approximated_x_max >= approximated_x_min,
                color=self._color,
                alpha=self._alpha,
            )
        else:
            self._ax.plot(approximated_x_min, z, color=self._color, alpha=self._alpha)
            self._ax.plot(approximated_x_max, z, color=self._color, alpha=self._alpha)

    def set_range(self, z_min: float, z_max: float) -> None:
        """
        近似された(Approximated)脚可動範囲の範囲を設定する．

        Parameters
        ----------
        z_min : float
            zの最小値．
        z_max : float
            zの最大値．
        """

        self._z_min = z_min
        self._z_max = z_max

        # z_minとz_maxの大小関係を確認
        if self._z_min > self._z_max:
            raise ValueError(
                "ApproximatedGraphRenderer.set_range: z_min is greater than z_max"
            )

    def set_draw_additional_line(self, draw_additional_line: bool) -> None:
        """
        補助線を描画するかどうかを設定する．

        Parameters
        ----------
        draw_additional_line : bool
            補助線を描画するか．
        """
        self._draw_additional_line = draw_additional_line

    def set_draw_fill(self, draw_fill: bool) -> None:
        """
        fillするかどうかを設定する．

        Parameters
        ----------
        draw_fill : bool
            fillするか．
        """
        self._draw_fill = draw_fill

    def set_color(self, color: str) -> None:
        """
        色を設定する．

        Parameters
        ----------
        color : str
            色．
        """
        self._color = color

    def set_alpha(self, alpha: float) -> None:
        """
        透明度を設定する．

        Parameters
        ----------
        alpha : float
            透明度．
        """
        self._alpha = alpha

        # 値が異常な場合は例外を投げる．
        if self._alpha < 0.0 or self._alpha > 1.0:
            raise ValueError(
                "ApproximatedGraphRenderer.set_alpha: alpha is out of range"
            )
