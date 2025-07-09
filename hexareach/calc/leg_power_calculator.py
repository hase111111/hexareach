"""
leg_power_calculator.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math
from typing import Any

import numpy as np
import numpy.typing as npt
import tqdm

from ..calc.hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..calc.hexapod_param_protocol import HexapodParamProtocol

class LegPowerCalculator:
    """
    脚先が出すことができる力を計算するクラス.
    """

    def __init__(
        self,
        hexapod_leg_range_calc: HexapodLegRangeCalculator,
        hexapod_param: HexapodParamProtocol):
        self._calc = hexapod_leg_range_calc
        self._param = hexapod_param


    def calculate(
        self,
        x_range: npt.NDArray[np.float64],
        z_range:npt.NDArray[np.float64]):
        """
        xとzの範囲内でロボットが出すことができる脚先の力を計算する.
        """
        # x*zの要素数を持つ2次元配列power_arrayを作成する(xが列，zが行)
        power_array = np.zeros((len(z_range), len(x_range)))
        # power_arrayの各要素に,x,zの座標における脚がだせる最大の力を計算して代入する，
        # 進捗表示のためにtqdmを使用する.必要なければ普通にrangeを使っても良い．
        for i in tqdm.tqdm(range(len(x_range))):
            for j in tqdm.tqdm(range(len(z_range)), leave=False):

                # j→i (z→x) の順で配列を参照することに注意．
                power_array[j][i] = self._get_max_power(x_range[i], z_range[j], 0, 1)

        return power_array

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
