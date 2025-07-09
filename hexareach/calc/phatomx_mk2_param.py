"""
phantomx_mk2_param.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math

from .hexapod_param_protocol import HexapodParamProtocol


class PhantomxMk2Param(HexapodParamProtocol):
    """
    Trossen Robotics 社製のロボット PhantomX MK2 のパラメータを持つクラス.
    """
    coxa_length: float = 52.0  # [mm]
    femur_length: float = 66.0  # [mm]
    tibia_length: float = 130.0  # [mm]
    theta1_max: float = math.radians(81.0)  # [rad]
    theta1_min: float = math.radians(-81.0)  # [rad]
    theta2_max: float = math.radians(99.0)  # [rad]
    theta2_min: float = math.radians(-105)  # [rad]
    theta3_max: float = math.radians(25.5)  # [rad]
    theta3_min: float = math.radians(-145.0)  # [rad]
    torque_max: float = 1800.0  # [N*mm] ストールトルク(停動トルク)
    approx_min_radius: float = 140.0  # [mm]
    approx_max_radius: float = 250.0  # [mm]
