"""
hexapod_leg_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import math
from typing import List

import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backend_bases import Event, MouseEvent
from matplotlib.table import Table

from .color_param import ColorParam
from .display_flag import DisplayFlag
from .circle_rednerer import CircleRenderer
from ..hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..calc.hexapod_param import HexapodParamProtocol

class HexapodLegRenderer:
    """
    脚の可動範囲を描画するクラス．
    """

    def __init__(
        self,
        hexapod_param: HexapodParamProtocol,
        fig: Figure,
        ax: Axes,
        ax_table: Axes,
        *,
        color_param: ColorParam = ColorParam(),
        display_flag: DisplayFlag = DisplayFlag()
    ) -> None:
        self._fig_name = "result/img.png"

        self._calc = HexapodLegRangeCalculator(hexapod_param)
        self._param = hexapod_param

        self._fig = fig
        self._ax = ax
        self._ax_table = ax_table
        self._color_param = color_param
        self._display_flag = display_flag

        self._wedge_r = 20.0  # 扇形の半径．

        # 脚の関節の位置．
        self._joint_pos: List[List[float]] = [
            [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]
        ]

        # クリックされたときに表示するグラフ用．
        self._joint_pos_click = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ]

        # 初期化フラグ．
        self._alreadly_init = False
        # 反転フラグ，逆運動学解の解が2つあるため，どちらを選ぶかを決める．
        self._reverse = False

        # 脚の可動範囲を表示するための円を登録．
        self._femur_circle = CircleRenderer(
            self._ax, self._param.femur_length,
            (0.0, 0.0),
            color="black",
            alpha=0.1,
        )
        self._tibia_circle = CircleRenderer(
            self._ax, self._param.tibia_length,
            (0.0, 0.0),
            color="black",
            alpha=0.1,
        )

        # 角度用の扇形を登録．
        self._femur_wedge = patch.Wedge((0.0, 0.0), self._wedge_r, 0, 10)
        self._tibia_wedge = patch.Wedge((0.0, 0.0), self._wedge_r, 0, 10)

        (self._leg_graph,) = self._ax.plot(  # type: ignore
            self._joint_pos[0], self._joint_pos[1])
        (self._leg_graph_click,) = self._ax.plot(  # type: ignore
            self._joint_pos[0], self._joint_pos[1])
        (self._error_joint,) = self._ax.plot(  # type: ignore
            self._joint_pos[0], self._joint_pos[1])

        # 角度を表示するためのテーブルを登録．
        self._angle_table: Table = self._ax_table.table(  # type: ignore
            cellText=[
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
            ],
            loc="center",
        )

    def render(self) -> None:
        """
        イベントを設定する,初期化処理.2度目以降の呼び出しは無視される．
        """

        print(f"{__name__}: Starts drawing the leg")
        print(f"{__name__}: {self._display_flag.leg_circle_displayed = }")
        print(f"{__name__}: {self._display_flag.leg_wedge_displayed = }")

        # すでに初期化済みの場合は何もしない．
        if self._alreadly_init:
            print(f"{__name__}: Already initialized.")
            return

        # 脚の付け根の円を描画．
        self._femur_circle.render()
        self._tibia_circle.render()

        self._femur_wedge.set_visible(self._display_flag.leg_wedge_displayed)
        self._tibia_wedge.set_visible(self._display_flag.leg_wedge_displayed)

        self._ax.add_artist(self._femur_wedge)
        self._ax.add_artist(self._tibia_wedge)

        # 脚の描画．
        self._leg_graph.set_linewidth(5)  # 太さを変える．
        self._leg_graph.set_marker("o")  # 点を描画する．
        self._leg_graph.set_markersize(10)  # 点の大きさを変える．

        self._leg_graph_click.set_linewidth(5)  # 太さを変える．
        self._leg_graph_click.set_marker("o")  # 点を描画する．
        self._leg_graph_click.set_markersize(10)  # 点の大きさを変える．
        self._leg_graph_click.set_visible(False)  # 非表示にする．

        # 可動範囲外の間接に色をつけるためのグラフ．
        self._error_joint.set_linewidth(0)  # 線を消す．
        self._error_joint.set_marker("o")  # 点を描画する．
        self._error_joint.set_markersize(12)  # 点の大きさを変える．
        self._error_joint.set_color("red")  # 色を変える．

        # マウスが動いたときに呼び出す関数を設定．
        self._fig.canvas.mpl_connect("motion_notify_event", self._on_update)

        # マウスが左クリックされたときに呼び出す関数を設定．
        self._fig.canvas.mpl_connect("button_press_event", self._on_click)

        self._ax_table.axis("off")
        self._ax_table.axis("tight")

        # 初期化済みフラグを立てる．
        self._alreadly_init = True

    def _on_update(self, event: Event) -> None:
        """マウスが動いたときに呼び出される関数．"""
        if not isinstance(event, MouseEvent):
            # マウスイベントでない場合は何もしない．
            return
        # マウスポイント地点を取得．
        mouse_x = event.xdata
        mouse_z = event.ydata

        if mouse_x is None or mouse_z is None:
            # マウスポイント地点が取得できなかった場合は何もしない．
            return

        # 脚の角度を計算．
        res, self._joint_pos, angle = self._calc.calc_inverse_kinematics_xz(
            mouse_x, mouse_z, self._reverse
        )
        self._leg_graph.set_data(self._joint_pos)
        self._leg_graph.set_visible(True)

        # 脚の付け根の円を描画．
        self._femur_circle.update_center((self._joint_pos[0][1], self._joint_pos[1][1]))
        self._tibia_circle.update_center((self._joint_pos[0][2], self._joint_pos[1][2]))

        # 扇形を描画．
        self._femur_wedge.set_center((self._joint_pos[0][1], self._joint_pos[1][1]))
        self._femur_wedge.set_theta1(min([0, math.degrees(angle[1])]))
        self._femur_wedge.set_theta2(max([0, math.degrees(angle[1])]))

        self._tibia_wedge.set_center((self._joint_pos[0][2], self._joint_pos[1][2]))
        self._tibia_wedge.set_theta1(
            min([math.degrees(angle[1]), math.degrees(angle[1] + angle[2])])
        )
        self._tibia_wedge.set_theta2(
            max([math.degrees(angle[1]), math.degrees(angle[1] + angle[2])])
        )

        # 失敗しているならば色を変える．
        if res:
            self._leg_graph.set_color("blue")

            # 可動範囲外ならばそのプロットの色を変える．
            if not self._calc.is_theta2_in_range(
                angle[1]
            ) or not self._calc.is_theta3_in_range(angle[2]):

                error_point: List[List[float]] = [[], []]

                if not self._calc.is_theta2_in_range(angle[1]):
                    error_point[0].append(self._joint_pos[0][1])
                    error_point[1].append(self._joint_pos[1][1])

                if not self._calc.is_theta3_in_range(angle[2]):
                    error_point[0].append(self._joint_pos[0][2])
                    error_point[1].append(self._joint_pos[1][2])

                self._error_joint.set_visible(True)
                self._error_joint.set_data(error_point)

            else:
                self._error_joint.set_visible(False)
        else:
            self._leg_graph.set_color("red")

        # 表を更新．
        self._angle_table._cells[(1, 1)]._text.set_text(  # type: ignore
            f"{math.degrees(angle[0]):.3f}")
        self._angle_table._cells[(2, 1)]._text.set_text(  # type: ignore
            f"{math.degrees(angle[1]):.3f}"
        )
        self._angle_table._cells[(3, 1)]._text.set_text(  # type: ignore
            f"{math.degrees(angle[2]):.3f}"
        )

        _, ar_s, ar_ls, ar_rs = self._calc.calc_inverse_kinematics_xz_arduino(
            mouse_x, -mouse_z
        )
        self._angle_table._cells[(4, 1)]._text.set_text(str(ar_s[0]))  # type: ignore
        self._angle_table._cells[(5, 1)]._text.set_text(str(ar_s[1]))  # type: ignore
        self._angle_table._cells[(6, 1)]._text.set_text(str(ar_s[2]))  # type: ignore

        table_error_color = "red"
        table_normal_color = "white"

        self._angle_table._cells[(7, 1)]._text.set_text(str(ar_ls[0]) + " (226 ~ 789)")  # type: ignore
        if ar_ls[0] < 226 or ar_ls[0] > 789:
            self._angle_table._cells[(7, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(7, 1)].set_facecolor(table_normal_color)  # type: ignore

        self._angle_table._cells[(8, 1)]._text.set_text(str(ar_ls[1]) + " (156 ~ 858)")  # type: ignore
        if ar_ls[1] < 156 or ar_ls[1] > 858:
            self._angle_table._cells[(8, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(8, 1)].set_facecolor(table_normal_color)  # type: ignore

        self._angle_table._cells[(9, 1)]._text.set_text(str(ar_ls[2]) + " (272 ~ 859)")  # type: ignore
        if ar_ls[2] < 272 or ar_ls[2] > 859:
            self._angle_table._cells[(9, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(9, 1)].set_facecolor(table_normal_color)  # type: ignore

        self._angle_table._cells[(10, 1)]._text.set_text(str(ar_rs[0]) + " (223 ~ 789)")  # type: ignore
        if ar_rs[0] < 223 or ar_rs[0] > 789:
            self._angle_table._cells[(10, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(10, 1)].set_facecolor(table_normal_color)  # type: ignore

        self._angle_table._cells[(11, 1)]._text.set_text(str(ar_rs[1]) + " (156 ~ 860)")  # type: ignore
        if ar_rs[1] < 156 or ar_rs[1] > 860:
            self._angle_table._cells[(11, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(11, 1)].set_facecolor(table_normal_color)  # type: ignore

        self._angle_table._cells[(12, 1)]._text.set_text(str(ar_rs[2]) + " (157 ~ 743)")  # type: ignore
        if ar_rs[2] < 157 or ar_rs[2] > 743:
            self._angle_table._cells[(12, 1)].set_facecolor(table_error_color)  # type: ignore
        else:
            self._angle_table._cells[(12, 1)].set_facecolor(table_normal_color)  # type: ignore

        # グラフを再描画．
        plt.draw()
        return

    def _on_click(self, event: Event):
        if not isinstance(event, MouseEvent):
            # マウスイベントでない場合は何もしない．
            return

        left_click_index = 1
        middle_click_index = 2
        right_click_index = 3

        # 右クリックされた場合は表示を消す．
        if event.button == right_click_index:
            self._leg_graph_click.set_visible(False)

        # 中クリックされた場合は反転．
        elif event.button == middle_click_index:
            self._reverse = not self._reverse
            self._on_update(event)

        # 左クリックされた場合は表示を更新．
        elif event.button == left_click_index:
            self._fig.savefig(self._fig_name, transparent=True)  #type: ignore
            self._leg_graph_click.set_visible(True)
            self._joint_pos_click = self._joint_pos
            self._leg_graph_click.set_data(self._joint_pos_click)

        plt.draw()

    def set_img_file_name(self, file_name: str) -> None:
        """
        画像を保存するときのファイル名を設定する.

        Parameters
        ----------
        file_name : str
            画像を保存するときのファイル名.
        """

        self._fig_name = file_name
