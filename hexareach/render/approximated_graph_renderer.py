"""
approximated_graph_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import matplotlib.axes as axes
import numpy as np

from .color_param import ColorParam
from ..hexapod_param import HexapodParamProtocol
from ..hexapod_leg_range_calculator import HexapodLegRangeCalculator


class ApproximatedGraphRenderer:

    def __init__(
        self,
        hexapod_param: HexapodParamProtocol,
        ax: axes.Axes,
        color_param: ColorParam = ColorParam(),
        z_min: float = -300,
        z_max: float = 300,
        draw_additional_line: bool = True,
    ) -> None:
        self._calc = HexapodLegRangeCalculator(hexapod_param)
        self._ax = ax
        self._color_param = color_param

        if self._ax is None:
            raise ValueError("ax is None")

        self._graph_step = 0.01
        self.set_draw_additional_line(draw_additional_line)
        self.set_range(z_min, z_max)

    def render(self) -> None:
        """
        近似された(Approximated)脚可動範囲の表示を行う．
        セット関数はこの関数の前に呼び出す必要がある．
        """

        print(f"{__name__}: Shows approximate leg range of motion")

        color = self._color_param.approximated_graph_color
        alpha = self._color_param.approximated_graph_alpha
        draw_fill = self._color_param.approximated_graph_filled

        # 近似された(Approximated)脚可動範囲の計算を行う．
        # GRAPH_STEP刻みでZ_MINからZ_MAXまでの配列zを作成．
        z = np.arange(self._z_min, self._z_max, self._graph_step)

        # xと同じ要素数で値がすべて min_leg_radius の配列zを作成．
        approximated_x_min = np.full_like(
            z, self._calc.get_approximate_min_leg_raudus()
        )

        approximated_x_max = []
        for i in range(len(z)):
            approximated_x_max.append(self._calc.get_approximate_max_leg_raudus(z[i]))

        if self._draw_additional_line:
            # 補助線を描画する．
            self._ax.plot(approximated_x_min, z, color=color, alpha=0.1)
            self._ax.plot(approximated_x_max, z, color=color, alpha=0.1)

        # xとzで囲まれた範囲をfillする．
        if draw_fill:
            self._ax.fill_betweenx(
                z,
                approximated_x_min,
                approximated_x_max,
                where=approximated_x_max >= approximated_x_min,
                color=color,
                alpha=alpha,
            )
        else:
            self._ax.plot(approximated_x_min, z, color=color, alpha=alpha)
            self._ax.plot(approximated_x_max, z, color=color, alpha=alpha)

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
