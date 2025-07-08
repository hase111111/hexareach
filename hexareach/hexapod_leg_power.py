"""
hexapod_leg_power.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import copy
import math
from typing import Any

from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import tqdm

from .calc.hexapod_leg_range_calculator import HexapodLegRangeCalculator
from .calc.hexapod_param_protocol import HexapodParamProtocol


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
        x_min: float = -300,
        x_max: float = 300,
        z_min: float = -300,
        z_max: float = 300
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
        self._calc = hexapod_leg_range_calc
        self._figure = figure
        self._ax = ax
        self.set_step(step)
        self.set_range(x_min, x_max, z_min, z_max)

        self._param = hexapod_param

    def render(self) -> None:
        """
        x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画する．\n
        力の大きさは，等高線で表現する．\n
        大変時間のかかる処理なので，実行には時間がかかる．\n
        """

        print(
            "HexapodLegPower.render: Draws the distribution of forces. "
            "Please wait 10 seconds for this time-consuming process."
        )
        print(
            "HexapodLegPower.render: "
            + "x_min = "
            + str(self._x_min)
            + "[mm], "
            + "x_max = "
            + str(self._x_max)
            + "[mm], "
            + "z_min = "
            + str(self._z_min)
            + "[mm], "
            + "z_max = "
            + str(self._z_max)
            + "[mm], "
            + "step = "
            + str(self._step)
            + "[mm], "
            + "torque_max = "
            + str(self._param.torque_max)
            + "[N*mm] "
        )

        # x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画するため，
        # min から max まで self.__step づつ増やした数値を格納した配列を作成する．
        x_range = np.arange(self._x_min, self._x_max + 1, self._step)
        z_range = np.arange(self._z_min, self._z_max + 1, self._step)

        # x*zの要素数を持つ2次元配列power_arrayを作成する(xが列，zが行)
        power_array = np.zeros((len(z_range), len(x_range)))

        # power_arrayの各要素に,x,zの座標における脚がだせる最大の力を計算して代入する，
        # 進捗表示のためにtqdmを使用する.必要なければ普通にrangeを使っても良い．
        for i in tqdm.tqdm(range(len(x_range))):
            for j in tqdm.tqdm(range(len(z_range)), leave=False):

                # j→i (z→x) の順で配列を参照することに注意．
                power_array[j][i] = self._get_max_power(x_range[i], z_range[j], 0, 1)

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

    def _get_max_power(
        self, x: float, z: float, power_x: float, power_z: float
    ) -> float:
        """
        x,zの座標における脚の力の最大値を返す

        Parameters
        ----------
        x : float
            脚先のx座標 [mm]
        z : float
            脚先のz座標 [mm]
        power_x : float
            x方向にかかる力.正規化されていること [N]
        power_z : float
            z方向にかかる力.正規化されていること [N]

        Returns
        -------
        ans : float
            引数で受け取った力を何倍したら，トルクが最大値を超えるか．\n倍率を返す．
        """

        # 逆運動学解．間接の角度を求める
        is_sucess, _, angle = self._calc.calc_inverse_kinematics_xz(x, z)

        # 逆運動学解が得られなかった場合は終了する
        if not is_sucess or (
            is_sucess
            and (
                not self._calc.is_theta2_in_range(angle[1])
                or not self._calc.is_theta3_in_range(angle[2])
            )
        ):

            # もう一つの逆運動学解を求める
            is_sucess, _, angle = self._calc.calc_inverse_kinematics_xz(x, z, True)

            if not is_sucess or (
                is_sucess
                and (
                    not self._calc.is_theta2_in_range(angle[1])
                    or not self._calc.is_theta3_in_range(angle[2])
                )
            ):
                return 0.0

        ans = 0

        # 逆運動学解が得られた場合は，トルクの計算をする
        power_list = np.arange(1, 20, 1)  # 6から12までの0.5刻みのリスト
        for p in power_list:

            # ヤコビ行列を作成
            jacobian = self._make_jacobian(angle[1], angle[2])

            # 力のベクトルを作成 [F_x, F_z]^T
            power = np.array([[float(power_x * p)], [float(power_z * p)]])

            # トルクを計算する [tauqe_femur, tauqe_tibia]^T
            tauqe = jacobian.T @ power  # t = J^T * F

            # トルクの絶対値を計算する
            femur_tauqe = math.fabs(tauqe[0][0])
            tibia_tauqe = math.fabs(tauqe[1][0])

            # トルクの最大値を超えていないか判定する．超えたら終了，超えていなければ記録して次のループへ．
            if (
                femur_tauqe < self._param.torque_max
                and tibia_tauqe < self._param.torque_max
            ):
                ans = p
            else:
                break

        return (float)(ans)

    def _make_jacobian(self, theta2: float, theta3: float) -> np.ndarray[Any, Any]:
        """
        ヤコビ行列を計算する．

        Parameters
        ----------
        theta2 : float
            第2間接の角度 [rad]
        theta3 : float
            第3間接の角度 [rad]

        Returns
        -------
        jacobian : np.ndarray
            2*2のヤコビ行列．
        """

        lf = self._param.femur_length
        lt = self._param.tibia_length

        # 2*2のヤコビ行列を作成
        jacobian = np.array(
            [
                [
                    -lf * math.sin(theta2) - lt * math.sin(theta2 + theta3),
                    -lt * math.sin(theta2 + theta3),
                ],
                [
                    lf * math.cos(theta2) + lt * math.cos(theta2 + theta3),
                    lt * math.cos(theta2 + theta3),
                ],
            ]
        )

        return jacobian

    def set_step(self, step: float) -> None:
        """
        何mmごとに力の分布を計算するかを設定する．

        Parameters
        ----------
        step : float
            何mmごとに力の分布を計算するか．
        """

        self._step = step

        if self._step < 1:
            raise ValueError(
                "HexapodLegPower.set_step: step is less than or equal to 1"
            )

    def set_range(self, x_min: float, x_max: float, z_min: float, z_max: float) -> None:
        """
        脚の可動範囲を設定する．

        Parameters
        ----------
        x_min : float
            x軸の最小値
        x_max : float
            x軸の最大値
        z_min : float
            z軸の最小値
        z_max : float
            z軸の最大値
        """

        self._x_min = x_min
        self._x_max = x_max
        self._z_min = z_min
        self._z_max = z_max

        if self._x_min >= self._x_max:
            raise ValueError("HexapodLegPower.set_range: x_min >= x_max")

        if self._z_min >= self._z_max:
            raise ValueError("HexapodLegPower.set_range: z_min >= z_max")
