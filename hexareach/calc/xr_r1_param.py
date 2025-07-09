"""
xr_r1_param.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math

from .hexapod_param_protocol import HexapodParamProtocol


class XrR1Param(HexapodParamProtocol):
    """
    XiaoR Geek社製のロボット XR-R1 のパラメータを持つクラス．
    参考 : https://www.xiaorgeek.net/products/
    """
    coxa_length: float = 45.0  # [mm]
    femur_length: float = 75.0  # [mm]
    tibia_length: float = 140.0  # [mm]
    theta1_max: float = math.radians(90.0)  # [rad]
    theta1_min: float = math.radians(-90.0)  # [rad]
    theta2_max: float = math.radians(90.0)  # [rad]
    theta2_min: float = math.radians(-90.0)  # [rad]
    theta3_max: float = math.radians(0.0)  # [rad]
    theta3_min: float = math.radians(-170.0)  # [rad]
    torque_max: float = 3400.0  # [N*mm] ストールトルク(停動トルク)
    approx_min_radius: float = 135.0  # [mm]
    approx_max_radius: float = 200.0  # [mm]
