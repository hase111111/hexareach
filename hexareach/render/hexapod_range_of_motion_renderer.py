"""
hexapod_range_of_motion_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import List, Optional, Any

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import numpy as np
from numpy.typing import NDArray

from ..calc.hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..calc.hexapod_param import HexapodParamProtocol
from .color_param import ColorParam


class HexapodRangeOfMotionRenderer:
    """
    脚の可動範囲を描画するクラス．
    """

    def __init__(
        self,
        hexapod_param: HexapodParamProtocol,
        fig: Figure,
        ax: Axes,
        *,
        color_param: ColorParam = ColorParam(),
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
        self._calc = HexapodLegRangeCalculator(hexapod_param)
        self._param = hexapod_param
        self._fig = fig
        self._ax = ax
        self._color_param = color_param
        self._step = 0.001

        self._upper_leg: Optional[List[Line2D]] = None
        self._lower_leg: Optional[List[Line2D]] = None

        # 上下どちらを色濃く描画するかを決めるためのフラグ
        self.switch_upper_lower: bool = True

    def render(self) -> None:
        """脚の可動範囲を描画する．"""

        print(f"{__name__}: Draw the range of motion of the legs")
        print(f"{__name__}: {self._color_param.leg_range_color = }")
        print(f"{__name__}: {self._color_param.leg_range_upper_alpha = }")
        print(f"{__name__}: {self._color_param.leg_range_lower_alpha = }")

        self.render_upper_leg_range()
        self.render_lower_leg_range()

        # マウス移動時に線を更新する関数を登録
        self._fig.canvas.mpl_connect("button_press_event", self._on_move)

    def _on_move(self, event: Any) -> None:
        """
        ホイールクリックで上向きの可動範囲と下向きの可動範囲を切り替える（再描画せずLine2Dの色・アルファ値のみ変更）．
        """
        # 中ボタン（ホイールクリック）以外は無視
        if not hasattr(event, "button") or event.button != 2:  # type: ignore
            return

        # フラグをトグル
        self.switch_upper_lower = not self.switch_upper_lower

        # 上下の可動範囲のLine2Dの色・アルファ値のみを切り替える
        if self._upper_leg is not None:
            for line in self._upper_leg:
                line.set_color(self._color_param.leg_range_color)
                if self.switch_upper_lower:
                    line.set_alpha(self._color_param.leg_range_upper_alpha)
                else:
                    line.set_alpha(self._color_param.leg_range_lower_alpha)
        if self._lower_leg is not None:
            for line in self._lower_leg:
                line.set_color(self._color_param.leg_range_color)
                if self.switch_upper_lower:
                    line.set_alpha(self._color_param.leg_range_lower_alpha)
                else:
                    line.set_alpha(self._color_param.leg_range_upper_alpha)

        # 再描画
        self._ax.figure.canvas.draw_idle()  # type: ignore

    def render_upper_leg_range(self) -> None:
        """逆運動学解2つのうち，上向きの可動範囲を描画する．"""

        self._make_leg_range(
            self._param.theta2_min,
            self._param.theta2_max,
            0,
            self._param.theta3_max,
            self._color_param.leg_range_color,
            self._color_param.leg_range_upper_alpha,
            is_upper=True,
        )

    def render_lower_leg_range(self) -> None:
        """逆運動学解2つのうち，下向きの可動範囲を描画する．"""

        self._make_leg_range(
            self._param.theta2_min,
            self._param.theta2_max,
            self._param.theta3_min,
            0,
            self._color_param.leg_range_color,
            self._color_param.leg_range_lower_alpha,
            is_upper=False,
        )

    def _make_leg_range(
        self,
        theta2_min: float,
        theta2_max: float,
        theta3_min: float,
        theta3_max: float,
        color_value: str,
        alpha_vaule: float,
        is_upper: bool,
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

        # minからmaxまでstep刻みで配列を作成.
        femur_range = np.arange(theta2_min, theta2_max, self._step)
        tibia_range = np.arange(theta3_min, theta3_max, self._step)

        # femur joint (min ~ max) , tibia joint (min).
        _1 = self._make_leg_line(femur_range, np.array([theta3_min]), color_value, alpha_vaule)

        # femur joint (min ~ max) , tibia joint (max).
        _2 = self._make_leg_line(femur_range, np.array([theta3_max]), color_value, alpha_vaule)

        # femur joint (min) , tibia joint (min ~ max).
        _3 = self._make_leg_line(np.array([theta2_min]), tibia_range, color_value, alpha_vaule)

        # femur joint (max) , tibia joint (min ~ max).
        _4 = self._make_leg_line(np.array([theta2_max]), tibia_range, color_value, alpha_vaule)

        # 1 ~ 4の結果をリストに追加する.
        if is_upper:
            if self._upper_leg is None:
                self._upper_leg = []
            self._upper_leg.extend(_1)
            self._upper_leg.extend(_2)
            self._upper_leg.extend(_3)
            self._upper_leg.extend(_4)
        else:
            if self._lower_leg is None:
                self._lower_leg = []
            self._lower_leg.extend(_1)
            self._lower_leg.extend(_2)
            self._lower_leg.extend(_3)
            self._lower_leg.extend(_4)

    def _make_leg_line(
        self,
        theta2: NDArray[np.float64],
        theta3: NDArray[np.float64],
        color_value: str,
        alpha_vaule: float,
    ) -> List[Line2D]:
        """
        間接を回しながら，脚先の座標をプロットしていく．

        Parameters
        ----------
        theta2 : np.ndarray or list[float]
            theta2の配列．
        theta3 : np.ndarray or list[float]
            theta3の配列．
        color_value : str
            色．
        alpha_vaule : float
            透明度．
        """

        line_x: List[float] = []
        line_z: List[float] = []

        for _, t2 in enumerate(theta2):
            for _, t3 in enumerate(theta3):
                res, x, z = self._calc.get_leg_position_xz(t2, t3)

                if res:
                    line_x.append(x)
                    line_z.append(z)

        return self._ax.plot(line_x, line_z, color=color_value, alpha=alpha_vaule)  # type: ignore
