"""
color_param.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

class ColorParam:
    """
    グラフの色に関するパラメータを格納するクラス.
    """

    mouse_grid_color: str = "black"
    mouse_grid_alpha: float = 1.0
    approximated_graph_color: str = "green"
    approximated_graph_alpha: float = 0.5
    leg_range_color: str = "black"
    leg_range_upper_alpha: float = 0.3
    leg_range_lower_alpha: float = 1.0
    leg_circle_color: str = "black"
    leg_circle_alpha: float = 0.1
