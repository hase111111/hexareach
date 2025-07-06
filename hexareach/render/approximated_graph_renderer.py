"""
approximated_graph_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import Tuple

from matplotlib import axes
import numpy as np

from .color_param import ColorParam
from .display_flag import DisplayFlag
from ..hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..hexapod_param import HexapodParamProtocol


class ApproximatedGraphRenderer:
    """
    脚の可動範囲の近似グラフを描画するクラス。
    このクラスは HexapodLegRangeCalculator を用いて脚の可動範囲の近似値を計算し、
    指定されたaxes上に描画を行う。
    """

    def __init__(
        self,
        hexapod_param: HexapodParamProtocol,
        ax: axes.Axes,
        *,
        color_param: ColorParam = ColorParam(),
        display_flag: DisplayFlag = DisplayFlag(),
        z_min_max: Tuple[float, float] = (-300.0, 300.0)
    ) -> None:
        """
        コンストラクタ

        Parameters
        ----------
        hexapod_param : HexapodParamProtocol
            六脚ロボットのパラメータ
        ax : matplotlib.axes.Axes
            描画対象のAxesオブジェクト
        color_param : ColorParam, optional
            グラフの色や透明度のパラメータ
        display_flag : DisplayFlag, optional
            描画オプションのフラグ
        z_min_max : Tuple[float, float], optional
            z軸方向の描画範囲（最小値, 最大値）
        """
        self._calc = HexapodLegRangeCalculator(hexapod_param)
        self._ax = ax
        self._color_param = color_param
        self._display_flag = display_flag
        self._graph_step = 0.01
        self._z_min = z_min_max[0]
        self._z_max = z_min_max[1]

        # z_min が z_max 以下かどうかをチェック。
        if self._z_min > self._z_max:
            raise ValueError(f"{__name__}: {self._z_min=} is greater than {self._z_max=}")

    def render(self) -> None:
        """
        脚の可動範囲の近似値を描画する。
        この関数を呼ぶ前に set_range 関数で範囲を設定しておく必要がある。
        """

        print(f"{__name__}: Starts drawing the approximated graph")

        color = self._color_param.approximated_graph_color
        alpha = self._color_param.approximated_graph_alpha
        draw_fill = self._display_flag.approximated_graph_filled

        # 脚の可動範囲の近似値を計算する。
        # z_min から z_max まで graph_step 間隔で z の配列を作成。
        z = np.arange(self._z_min, self._z_max, self._graph_step)

        # z と同じ要素数で、すべて min_leg_radius の値を持つ配列を作成。
        approximated_x_min = np.full_like(
            z, self._calc.get_approximate_min_leg_raudus()
        )

        # 空の配列を作成。
        approximated_x_max = np.empty([0])

        for _, z_value in enumerate(z):
            approximated_x_max = np.append(
                approximated_x_max,
                self._calc.get_approximate_max_leg_raudus(z_value),
            )

        # x, z で囲まれた領域を塗りつぶす。
        if draw_fill:
            self._ax.fill_betweenx(  # type: ignore
                z,
                approximated_x_min,
                approximated_x_max,
                where=(approximated_x_max >= approximated_x_min).tolist(),
                color=color,
                alpha=alpha,
            )
        else:
            self._ax.plot(  # type: ignore
                approximated_x_min, z, color=color, alpha=alpha)
            self._ax.plot(  # type: ignore
                approximated_x_max, z, color=color, alpha=alpha)
