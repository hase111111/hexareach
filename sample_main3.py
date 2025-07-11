"""
sample_main3.py
ロボットのパラメータを変更して表示する場合のサンプルプログラム.
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


import math

import hexareach as hxr


if __name__ == "__main__":
    class OriginalRobotParam(hxr.HexapodParamProtocol):
        """
        このような形で可動範囲を計算したいロボット用に,
        HexapodParamProtocolを継承したクラスを作成すること.
        """

        coxa_length: float = 0.0  # [mm]
        femur_length: float = 100.0  # [mm]
        tibia_length: float = 100.0  # [mm]
        theta1_max: float = math.radians(0.0)  # [rad]
        theta1_min: float = math.radians(0.0)  # [rad]
        theta2_max: float = math.radians(100.0)  # [rad]
        theta2_min: float = math.radians(-100)  # [rad]
        theta3_max: float = math.radians(100.0)  # [rad]
        theta3_min: float = math.radians(-100.0)  # [rad]
        torque_max: float = 0.0  # [N*mm] ストールトルク(停動トルク)
        approx_min_radius: float = 0  # [mm]
        approx_max_radius: float = 250.0  # [mm]

    graph = hxr.GraphDisplayer()
    param = OriginalRobotParam()

    flag = hxr.DisplayFlag()
    flag.display_table = False
    flag.display_approximated_graph = False

    # rect を変更することで，描画領域を調整することができます.
    graph.display(
        param,
        display_flag=flag,
        rect=(-250.0, 250.0, -250.0, 250.0),
        image_file_name="result/sample_main3.png")
