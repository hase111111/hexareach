"""
clamp_angle.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math

def clamp_angle(angle: float) -> float:
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
    while angle > math.pi or angle < -math.pi:
        if angle > math.pi:
            angle -= math.pi * 2.0
        elif angle < -math.pi:
            angle += math.pi * 2.0
    return angle
