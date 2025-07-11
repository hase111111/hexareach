"""
leg_param_table.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math
from typing import List, Dict, Tuple, Optional

from matplotlib.axes import Axes
from matplotlib.table import Cell

class LegParamTable:
    """
    脚のパラメータを表示するためのテーブルを管理するクラス.
    このクラスは脚の各関節の角度や位置などのパラメータを表示するためのテーブルを生成し,
    更新する機能を提供します.
    """

    def __init__(self, ax: Optional[Axes]) -> None:
        if ax is None:
            self._show = False
            return

        self._ax = ax

        table_data = [
            ["Joint", "Angle [deg]"],
            ["coxa", ""],
            ["femur", ""],
            ["tibia", ""],
            ["coxa servo", ""],
            ["femur servo", ""],
            ["tibia servo", ""],
            ["left coxa servo", ""],
            ["left femur servo", ""],
            ["left tibia servo", ""],
            ["right coxa servo", ""],
            ["right femur servo", ""],
            ["right tibia servo", ""],
        ]

        self._table = self._ax.table(  # type: ignore
            cellText=table_data,
            colLabels=None,
            loc='center',
            cellLoc='center'
        )

        self._ax.axis("off")
        self._ax.axis("tight")

        self._cell_info: Dict[Tuple[int, int], Cell] = {}

        for (i, j), cell in self._table.get_celld().items():
            if i >= 0 and j >= 0:
                self._cell_info[(i, j)] = cell

        self._show = True


    def on_update(
            self,
            joint_angles: List[float],
            ar_s: List[int],
            ar_ls: List[int],
            ar_rs: List[int]) -> None:
        """
        テーブルの内容を更新するメソッド.
        """
        if not self._show:
            return

        self._cell_info[(1, 1)].set_text_props(  # type: ignore
            text=f"{math.degrees(joint_angles[0]):.3f}"
        )
        self._cell_info[(2, 1)].set_text_props(  # type: ignore
            text=f"{math.degrees(joint_angles[1]):.3f}"
        )
        self._cell_info[(3, 1)].set_text_props(  # type: ignore
            text=f"{math.degrees(joint_angles[2]):.3f}"
        )

        self._cell_info[(4, 1)].set_text_props(text=str(ar_s[0]))  # type: ignore
        self._cell_info[(5, 1)].set_text_props(text=str(ar_s[1]))  # type: ignore
        self._cell_info[(6, 1)].set_text_props(text=str(ar_s[2]))  # type: ignore

        table_error_color = "red"
        table_normal_color = "white"

        self._cell_info[(7, 1)].set_text_props(text=str(ar_ls[0]))  # type: ignore
        if ar_ls[0] < 226 or ar_ls[0] > 789:
            self._cell_info[(7, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(7, 1)].set_facecolor(table_normal_color)

        self._cell_info[(8, 1)].set_text_props(text=str(ar_ls[1]))  # type: ignore
        if ar_ls[1] < 156 or ar_ls[1] > 858:
            self._cell_info[(8, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(8, 1)].set_facecolor(table_normal_color)

        self._cell_info[(9, 1)].set_text_props(text=str(ar_ls[2]))  # type: ignore
        if ar_ls[2] < 272 or ar_ls[2] > 859:
            self._cell_info[(9, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(9, 1)].set_facecolor(table_normal_color)

        self._cell_info[(10, 1)].set_text_props(text=str(ar_rs[0]))  # type: ignore
        if ar_rs[0] < 223 or ar_rs[0] > 789:
            self._cell_info[(10, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(10, 1)].set_facecolor(table_normal_color)

        self._cell_info[(11, 1)].set_text_props(text=str(ar_rs[1]))  # type: ignore
        if ar_rs[1] < 156 or ar_rs[1] > 860:
            self._cell_info[(11, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(11, 1)].set_facecolor(table_normal_color)

        self._cell_info[(12, 1)].set_text_props(text=str(ar_rs[2]))  # type: ignore
        if ar_rs[2] < 157 or ar_rs[2] > 743:
            self._cell_info[(12, 1)].set_facecolor(table_error_color)
        else:
            self._cell_info[(12, 1)].set_facecolor(table_normal_color)
