"""
display_flag.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

class DisplayFlag:
    """
    グラフの表示に関するフラグを格納するクラス.
    """

    approximated_graph_filled: bool = True
    leg_circle_displayed: bool = True
    leg_wedge_displayed: bool = True
    display_table: bool = True
    display_leg_power: bool = False
    display_approximated_graph: bool = False
    display_mouse_grid: bool = True
    display_ground_line: bool = False
