"""
hexapod_param.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import Protocol


class HexapodParamProtocol(Protocol):
    """
    Protocol for storing Hexapod parameters.
    The HexapodParam class implements this protocol.
    """
    coxa_length: float
    femur_length: float
    tibia_length: float
    theta1_max: float
    theta1_min: float
    theta2_max: float
    theta2_min: float
    theta3_max: float
    theta3_min: float
    torque_max: float
    approx_min_radius: float
