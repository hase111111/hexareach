"""
hexapod_range_of_motion.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import List

import matplotlib.axes as axes
import numpy as np

from .hexapod_leg_range_calculator import HexapodLegRangeCalculator
from .hexapod_param import HexapodParam


class HexapodRangeOfMotion:

    def __init__(
        self,
        hexapod_leg_range_calc: HexapodLegRangeCalculator,
        hexapod_param: HexapodParam,
        ax: axes.Axes,
        *,
        color: str = "black",
        upper_alpha: float = 0.3,
        lowwer_alpha: float = 1.0
    ) -> None:
        """
        Parameters
        ----------
        hexapod_leg_range_calc : HexapodLegRangeCalculator
            脚の可動範囲を計算するためのインスタンス．
        hexapod_param : HexapodParam
            パラメータを格納するためのインスタンス．
        ax : matplotlib.axes.Axes
            matplotlibのaxesオブジェクト．
        color : str
            色．
        upper_alpha : float
            上向きの可動範囲の透明度．
        lowwer_alpha : float
            下向きの可動範囲の透明度．
        """
        self._calc = hexapod_leg_range_calc
        self._param = hexapod_param
        self._ax = ax

        self.set_color(color)
        self.set_upper_alpha(upper_alpha)
        self.set_lowwer_alpha(lowwer_alpha)

        self._STEP = 0.001

        # 例外を投げる
        if self._calc is None:
            raise ValueError("hexapod_leg_range_calc is None")

        if self._param is None:
            raise ValueError("hexapod_param is None")

        if self._ax is None:
            raise ValueError("ax is None")

    def render(self) -> None:
        """脚の可動範囲を描画する．"""

        print("HexapodLegRangeCalculator.render: Draw the range of motion of the legs")
        print(
            "HexapodLegRangeCalculator.render: "
            + "color: "
            + self._color
            + ", "
            + "upper_alpha: "
            + str(self._upper_alpha)
            + ", lowwer_alpha: "
            + str(self._lowwer_alpha)
            + ", (step: "
            + str(self._STEP)
            + ")"
        )

        self.render_upper_leg_range()
        self.render_lower_leg_range()

    def render_upper_leg_range(self) -> None:
        """逆運動学解2つのうち，上向きの可動範囲を描画する．"""

        self._make_leg_range(
            self._param.theta2_min,
            self._param.theta2_max,
            0,
            self._param.theta3_max,
            self._color,
            self._upper_alpha,
        )

    def render_lower_leg_range(self) -> None:
        """逆運動学解2つのうち，下向きの可動範囲を描画する．"""

        self._make_leg_range(
            self._param.theta2_min,
            self._param.theta2_max,
            self._param.theta3_min,
            0,
            self._color,
            self._lowwer_alpha,
        )

    def set_color(self, color: str) -> None:
        """
        色を設定する．

        Parameters
        ----------
        color : str
            色．
        """

        self._color = color

    def set_upper_alpha(self, alpha: float) -> None:
        """
        上向きの可動範囲の透明度を設定する．

        Parameters
        ----------
        alpha : float
            透明度．
        """

        self._upper_alpha = alpha

        # 例外を投げる
        if self._upper_alpha < 0 or self._upper_alpha > 1:
            raise ValueError(
                "The value of upper_alpha is out of range. The value must be between 0 and 1."
            )

    def set_lowwer_alpha(self, alpha: float) -> None:
        """
        下向きの可動範囲の透明度を設定する．

        Parameters
        ----------
        alpha : float
            透明度．
        """

        self._lowwer_alpha = alpha

        # 例外を投げる
        if self._lowwer_alpha < 0 or self._lowwer_alpha > 1:
            raise ValueError(
                "The value of lowwer_alpha is out of range. The value must be between 0 and 1."
            )

    def _make_leg_range(
        self,
        theta2_min: float,
        theta2_max: float,
        theta3_min: float,
        theta3_max: float,
        color_value: str,
        alpha_vaule: float,
    ) -> None:
        """
        脚の可動範囲を描画する．\n
        1つの間接を最大値に固定して,もう一つの間接を最小値から最大値まで動かす．\n
        次に,最小値に固定して,もう一つの間接を最小値から最大値まで動かす．\n
        今度は逆にして描画を行うと,脚の可動範囲が描画できる．

        Parameters
        ----------
        theta2_min : float
            theta2の最小値．
        theta2_max : float
            theta2の最大値．
        theta3_min : float
            theta3の最小値．
        theta3_max : float
            theta3の最大値．
        color_value : str
            色．
        alpha_vaule : float
            透明度．
        """

        # minからmaxまでstep刻みで配列を作成
        femur_range = np.arange(theta2_min, theta2_max, self._STEP)
        tibia_range = np.arange(theta3_min, theta3_max, self._STEP)

        # femur joint (min ~ max) , tibia joint (min)
        self._make_leg_line(femur_range, [theta3_min], color_value, alpha_vaule)

        # femur joint (min ~ max) , tibia joint (max)
        self._make_leg_line(femur_range, [theta3_max], color_value, alpha_vaule)

        # femur joint (min) , tibia joint (min ~ max)
        self._make_leg_line([theta2_min], tibia_range, color_value, alpha_vaule)

        # femur joint (max) , tibia joint (min ~ max)
        self._make_leg_line([theta2_max], tibia_range, color_value, alpha_vaule)

    def _make_leg_line(
        self,
        theta2: List[float],
        theta3: List[float],
        color_value: str,
        alpha_vaule: float,
    ) -> None:
        """
        間接を回しながら，脚先の座標をプロットしていく．

        Parameters
        ----------
        theta2 : List[float]
            theta2の配列．
        theta3 : List[float]
            theta3の配列．
        color_value : str
            色．
        alpha_vaule : float
            透明度．
        """

        line_x = []
        line_z = []

        for i in range(len(theta2)):
            for j in range(len(theta3)):
                res = self._calc.get_leg_position_xz(theta2[i], theta3[j])

                if res[0]:
                    line_x.append(res[1])
                    line_z.append(res[2])

        self._ax.plot(line_x, line_z, color=color_value, alpha=alpha_vaule)
