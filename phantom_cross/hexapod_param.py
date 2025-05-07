# Copyright (c) 2023 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math


class HexapodParam:
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
