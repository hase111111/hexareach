"""
hexapod_leg_range_calculator.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math

from typing import Tuple, List

from .math.triangle_checker import TriangleChecker
from .hexapod_param import HexapodParamProtocol


class HexapodLegRangeCalculator:

    def __init__(self, hexapod_param: HexapodParamProtocol) -> None:
        """
        Parameters
        ----------
        hexapod_param : HexapodParamProtocol
            パラメータを格納するためのインスタンス．
        """
        self._DEBUG_FLAG = False
        self._param = hexapod_param
        self._init_approximate_max_leg_raudus()  # 脚の最大半径を計算する．

        if self._param is None:
            raise ValueError("param_instance is None")

        self._min_radius = self._param.approx_min_radius

        if self._min_radius < 0:
            raise ValueError("r must be greater than 0")

    def set_approximate_min_leg_raudus(self, r: float) -> None:
        """
        脚の最小半径を設定する．

        Parameters
        ----------
        r : float
            脚の最小半径 [mm]
        """

        self._min_radius = r

        # 異常な値の場合は例外を投げる．
        if self._min_radius < 0:
            raise ValueError("r must be greater than 0")

        return

    def get_approximate_min_leg_raudus(self) -> float:
        """
        脚の最小半径を返す．

        Returns
        -------
        res : float
            脚の最小半径 [mm]
        """

        return self._min_radius

    def get_approximate_max_leg_raudus(self, z: float) -> float:
        """
        脚の最大半径を返す．

        Parameters
        ----------
        z : float
            z座標 [mm]

        Returns
        -------
        res : float
            脚がx方向に脚を伸ばせる最大半径 [mm]
        """

        # zが範囲外の場合は0を返す
        if -z < 0 or len(self._approximate_max_leg_raudus) < -z:
            return self._min_radius

        # Z軸の座標軸の取り方が逆なので、zを反転させる
        r = self._approximate_max_leg_raudus[(int)(-z)]

        if self._min_radius < r:
            return r
        else:
            return self._min_radius

    def get_leg_position_xz(
        self, theta2: float, theta3: float
    ) -> Tuple[bool, float, float]:
        """
        第1関節の角度を無視して、第2関節と第3関節の角度から脚先の位置を計算する．\n
        出力は計算できたかを表すboolean,x,z平面における座標のタプル．

        Parameters
        ----------
        theta2 : float
            第2関節の角度 [rad]
        theta3 : float
            第3関節の角度 [rad]

        Returns
        -------
        res : Tuple[bool, float, float]
            間接の可動範囲外の場合はfalseを返す．\n
            脚先の位置のタプル,x[mm],z[mm]．
        """

        # 間接の可動範囲外の場合はFalseを返す
        if not self.is_theta2_in_range(theta2):
            return (False, 0.0, 0.0)
        if not self.is_theta3_in_range(theta3):
            return (False, 0.0, 0.0)

        # 脚の位置を計算する
        x = (
            self._param.coxa_length
            + self._param.femur_length * math.cos(theta2)
            + self._param.tibia_length * math.cos(theta2 + theta3)
        )
        z = self._param.femur_length * math.sin(
            theta2
        ) + self._param.tibia_length * math.sin(theta2 + theta3)
        return (True, x, z)

    def calc_inverse_kinematics_xz(
        self, x: float, z: float, reverse_flag: bool = False
    ) -> Tuple[bool, List[Tuple[float, float]], List[float]]:
        """
        逆運動学を計算する．

        Parameters
        ----------
        x : float
            脚の付け根から見た脚先のx座標 [mm]
        z : float
            脚の付け根から見た脚先のz座標 [mm]
        reverse_flag : bool
            逆運動学解は2つあるが、どちらを選択するかを決めるフラグ.Trueにすると脚先が上を向く.

        Returns
        -------
        res : Tuple[bool, List[Tuple[float, float]], List[float]]
            脚がとどかず計算できなければfalse,trueでも可動範囲外になることがある．\n
            脚の関節の座標のタプルのリスト,coxa(付け根),femur,tibia,脚先の順 x[mm],z[mm]\n
            脚の関節の角度のリスト,coxa(今回は0で固定),femur,tibiaの順 [rad]\n
        """
        joint_pos = [[], []]
        angle: List[float] = []

        # 脚の付け根．
        joint_pos[0].append(0)
        joint_pos[1].append(0)

        # 第1関節．
        joint_pos[0].append(self._param.coxa_length)
        joint_pos[1].append(0)
        angle.append(0)

        # 長さが足りない場合は計算できない．
        triangle_checker = TriangleChecker()
        if not triangle_checker.check(
            self._param.tibia_length,
            self._param.femur_length,
            math.sqrt(math.pow(x - self._param.coxa_length, 2.0) + math.pow(z, 2.0)),
        ):
            angle_ft: float  = math.atan2(z, x - self._param.coxa_length)
            angle_ft_phase: float  = angle_ft + math.pi  # 180度位相をずらす．
            angle_ft_phase = (
                angle_ft_phase > math.pi * 2.0
                and angle_ft_phase - math.pi * 2.0
                or angle_ft_phase
            )

            # 候補点を計算．
            candidate_x = joint_pos[0][1] + (
                self._param.femur_length + self._param.tibia_length
            ) * math.cos(angle_ft)
            candidate_z = joint_pos[1][1] + (
                self._param.femur_length + self._param.tibia_length
            ) * math.sin(angle_ft)

            candidate_x_phase = (
                joint_pos[0][1]
                + self._param.femur_length * math.cos(angle_ft_phase)
                + self._param.tibia_length * math.cos(angle_ft)
            )
            candidate_z_phase = (
                joint_pos[1][1]
                + self._param.femur_length * math.sin(angle_ft_phase)
                + self._param.tibia_length * math.sin(angle_ft)
            )

            # 候補点との距離を計算．
            distance = math.sqrt(
                math.pow(candidate_x - x, 2.0) + math.pow(candidate_z - z, 2.0)
            )
            distance_phase = math.sqrt(
                math.pow(candidate_x_phase - x, 2.0)
                + math.pow(candidate_z_phase - z, 2.0)
            )

            # 距離が近い方を選択．
            angle_f: float = angle_ft
            angle_t: float  = 0.0

            if distance > distance_phase:
                angle_f = angle_ft_phase
                angle_t = -math.pi

            joint_pos[0].append(
                joint_pos[0][1] + self._param.femur_length * math.cos(angle_f)
            )
            joint_pos[1].append(
                joint_pos[1][1] + self._param.femur_length * math.sin(angle_f)
            )

            joint_pos[0].append(
                joint_pos[0][2] + self._param.tibia_length * math.cos(angle_f + angle_t)
            )
            joint_pos[1].append(
                joint_pos[1][2] + self._param.tibia_length * math.sin(angle_f + angle_t)
            )

            angle.append(angle_f)
            angle.append(angle_t)

            return False, joint_pos, angle

        # 第2関節．
        coxa_to_leg_end = math.sqrt(
            math.pow(x - self._param.coxa_length, 2.0) + math.pow(z, 2.0)
        )
        q1 = math.atan2(z, x - self._param.coxa_length)
        q2_upper = (
            math.pow(self._param.femur_length, 2.0)
            + math.pow(coxa_to_leg_end, 2.0)
            - math.pow(self._param.tibia_length, 2.0)
        )
        q2_lower = 2.0 * self._param.femur_length * coxa_to_leg_end

        q2 = math.acos(q2_upper / q2_lower)
        if reverse_flag:
            q2 = -q2
        angle.append(q1 + q2)
        angle[1] = self._clamp_angle(angle[1])  # -180度～180度に収める．
        joint_pos[0].append(
            (self._param.femur_length * math.cos(angle[1])) + joint_pos[0][1]
        )
        joint_pos[1].append(
            (self._param.femur_length * math.sin(angle[1])) + joint_pos[1][1]
        )

        # 第3関節．
        joint_pos[0].append(x)
        joint_pos[1].append(z)
        angle.append(
            math.atan2(
                (joint_pos[1][3] - joint_pos[1][2]), (joint_pos[0][3] - joint_pos[0][2])
            )
            - angle[1]
        )
        angle[2] = self._clamp_angle(angle[2])  # -180度～180度に収める．
        return True, joint_pos, angle

    def calc_inverse_kinematics_xz_arduino(
        self, x: float, z: float
    ) -> Tuple[List[float], List[float], List[float], List[float]]:
        """
        coxa jointが回転していない場合の逆運動学を計算する．
        脚が水平に伸びる方向にx,上方向にzをとる．
        Arduinoのプログラムの移植,どのように離散化を行うかの可視化のため．

        Parameters
        ----------
        x : float
            脚の付け根から見た脚先のx座標 [mm]
        z : float
            脚の付け根から見た脚先のz座標 [mm]

        Returns
        -------
        res : Tuple[List[float], List[float], List[float], List[float]]
            3つの関節の角度のリスト,coxa,femur,tibiaの順 [rad]\n
            3つの関節のサーボ角のリスト,coxa,femur,tibiaの順 [0~1023],実際にはサーボが傾いてついているのでこの値をそのまま使用しない\n
            3つの関節の左足サーボ角のリスト,coxa,femur,tibiaの順 [0~1023]\n
            3つの関節の右足サーボ角のリスト,coxa,femur,tibiaの順 [0~1023]\n
        """
        angle = []
        angle.append(0.0)  # 第1関節の角度は0度．

        true_x = x - self._param.coxa_length
        im = math.sqrt(math.pow(true_x, 2) + math.pow(z, 2))  # length of imaginary leg.

        # get femur angle above horizon...
        q1 = -math.atan2(z, true_x)
        d1 = (
            math.pow(self._param.femur_length, 2)
            - math.pow(self._param.tibia_length, 2)
            + math.pow(im, 2)
        )
        d2 = 2 * self._param.femur_length * im
        try:
            q2 = math.acos(d1 / d2)
        except:
            q2 = 0.0
        angle.append(q1 + q2)

        # and tibia angle from femur...
        d1 = (
            math.pow(self._param.femur_length, 2)
            - math.pow(im, 2)
            + math.pow(self._param.tibia_length, 2)
        )
        d2 = 2 * self._param.tibia_length * self._param.femur_length
        try:
            angle.append(math.acos(d1 / d2) - math.pi / 2)
        except:
            angle.append(0.0)

        servo_angle = []
        servo_angle.append((int)(angle[0] * 100.0 / 51.0 * 100.0))
        servo_angle.append((int)(angle[1] * 100.0 / 51.0 * 100.0))
        servo_angle.append((int)(angle[2] * 100.0 / 51.0 * 100.0))

        left_servo_angle = []
        left_servo_angle.append(512 - servo_angle[0])
        left_servo_angle.append(500 - servo_angle[1])
        left_servo_angle.append(670 - servo_angle[2])

        right_servo_angle = []
        right_servo_angle.append(512 + servo_angle[0])
        right_servo_angle.append(524 + servo_angle[1])
        right_servo_angle.append(354 + servo_angle[2])

        return angle, servo_angle, left_servo_angle, right_servo_angle

    def is_theta1_in_range(self, theta1: float) -> bool:
        """
        第1関節の角度が範囲内かを判定する.
        """

        if theta1 < self._param.theta1_min or theta1 > self._param.theta1_max:
            return False
        return True

    def is_theta2_in_range(self, theta2: float) -> bool:
        """
        第2関節の角度が範囲内かを判定する.
        """

        if theta2 < self._param.theta2_min or theta2 > self._param.theta2_max:
            return False
        return True

    def is_theta3_in_range(self, theta3: float) -> bool:
        """
        第3関節の角度が範囲内かを判定する.
        """

        if theta3 < self._param.theta3_min or theta3 > self._param.theta3_max:
            return False
        return True

    def _init_approximate_max_leg_raudus(self) -> None:
        """
        脚の最大半径を計算する privateメソッド.
        """

        # 近似された脚の可動範囲の最大半径のリスト，z軸の座標軸の取り方が逆なので，zを反転させる．
        self._approximate_max_leg_raudus = []

        z_min = 0
        z_max = int(self._param.femur_length + self._param.tibia_length)
        x_min = int(self._param.coxa_length)
        x_max = int(
            self._param.coxa_length
            + self._param.femur_length
            + self._param.tibia_length
        )

        # 全て0で初期化．
        for z in range(z_min, z_max):
            self._approximate_max_leg_raudus.append(0.0)

        # 脚の最大半径を計算する．
        for z in range(z_min, z_max):
            for x in range(x_min, x_max):
                line_end_x = (float)(x)
                line_end_y = 0
                line_end_z = (float)(z)

                ik_true_x = (
                    math.sqrt(math.pow(line_end_x, 2.0) + math.pow(line_end_y, 2.0))
                    - self._param.coxa_length
                )
                im = math.sqrt(math.pow(ik_true_x, 2.0) + math.pow(line_end_z, 2.0))
                if im == 0:
                    im += 0.0000001

                q1 = -math.atan2(line_end_z, ik_true_x)
                q2_upper = (
                    math.pow(self._param.femur_length, 2.0)
                    + math.pow(im, 2.0)
                    - math.pow(self._param.tibia_length, 2.0)
                )
                q2_lower = 2.0 * self._param.femur_length * im
                q2_theta = q2_upper / q2_lower

                if (q2_theta < -1.0) or (q2_theta > 1.0):
                    if self._DEBUG_FLAG:
                        print(
                            "[error] : q2_theta:"
                            + str(q2_theta)
                            + " x:"
                            + str(x)
                            + " z:"
                            + str(z)
                        )
                    continue
                q2 = math.acos(q2_theta)

                r_margin = 1.0
                self._approximate_max_leg_raudus[z] = (float)(x) - r_margin

        return

    def _clamp_angle(self, angle: float) -> float:
        """
        角度を-180 ~ 180の範囲にする.

        Parameters
        ----------
        angle : float
            角度 [rad]

        Returns
        -------
        res : float
            角度 [rad]
        """
        if angle > math.pi:
            angle -= math.pi * 2.0
        elif angle < -math.pi:
            angle += math.pi * 2.0
        return angle
