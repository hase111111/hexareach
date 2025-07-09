"""
__init__.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


from .triangle_checker import TriangleChecker
from .clamp_angle import clamp_angle

__all__ = [
    "TriangleChecker",
    "clamp_angle"
]
