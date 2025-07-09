"""
hexapod_leg_power.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import copy
from typing import Tuple

from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import numpy.typing as npt

from ..calc.hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..calc.hexapod_param_protocol import HexapodParamProtocol
from ..calc.leg_power_calculator import LegPowerCalculator

class HexapodLegPower:
    """
    脚の力の分布を描画するクラス．
    """

    def __init__(
        self,
        hexapod_leg_range_calc: HexapodLegRangeCalculator,
        hexapod_param: HexapodParamProtocol,
        figure: Figure,
        ax: Axes,
        *,
        step: float = 1.0,
        rect: Tuple[float, float, float, float] = (-100.0, 300.0, -200.0, 200.0),
    ) -> None:
        """
        Parameters
        ----------
        hexapod_leg_range_calc : HexapodLegRangeCalculator
            脚の可動範囲を計算するためのインスタンス
        hexapod_param : HexapodParam
            パラメータを格納するためのインスタンス
        figure : plt.Figure
            matplotlibのfigureオブジェクト
        ax : matplotlib.axes.Axes
            matplotlibのaxesオブジェクト
        step : float
            何mmごとに力の分布を計算するか
        x_min : float
            x軸の最小値
        x_max : float
            x軸の最大値
        z_min : float
            z軸の最小値
        z_max : float
            z軸の最大値
        """
        self._figure = figure
        self._ax = ax
        self._x_min = rect[0]
        self._x_max = rect[1]
        self._z_min = rect[2]
        self._z_max = rect[3]
        self._step = step
        self._param = hexapod_param
        self._calc = LegPowerCalculator(hexapod_leg_range_calc, hexapod_param)

        if self._step < 1:
            raise ValueError(
                f"{__name__}: step is less than or equal to 1"
            )

        if self._x_min >= self._x_max:
            raise ValueError(f"{__name__}: x_min >= x_max")

        if self._z_min >= self._z_max:
            raise ValueError(f"{__name__}: z_min >= z_max")

    def render(self) -> None:
        """
        x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画する．\n
        力の大きさは，等高線で表現する．\n
        大変時間のかかる処理なので，実行には時間がかかる．\n
        """

        print(
            f"{__name__}: Draws the distribution of forces. "
            "Please wait about 10 seconds for this time-consuming process."
        )
        print(
            f"{__name__}: {self._x_min =}[mm], {self._x_max =}[mm], "
            f"{self._z_min =}[mm], {self._z_max =}[mm], "
            f"{self._step =}[mm], {self._param.torque_max = }")

        # x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画するため，
        # min から max まで self.__step づつ増やした数値を格納した配列を作成する．
        x_range: npt.NDArray[np.float_] = np.arange(self._x_min, self._x_max + 1, self._step)
        z_range: npt.NDArray[np.float_] = np.arange(self._z_min, self._z_max + 1, self._step)

        # x*zの要素数を持つ2次元配列power_arrayを作成する(xが列，zが行)
        power_array = self._calc.calculate(x_range, z_range)

        # power_arrayを等高線で描画する
        cmap = copy.copy(cm.get_cmap("jet"))
        cmap.set_under("silver")
        cmap.set_over("silver")
        power_contourf = self._ax.contourf(  # type: ignore
            x_range, z_range, power_array, cmap=cmap, levels=20, vmin=4.0, vmax=20.0
        )

        # カラーバーを表示する
        cbar = self._figure.colorbar(power_contourf)  # type: ignore
        cbar.set_label("[N]", fontsize=20)  # type: ignore
