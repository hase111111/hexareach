"""
graph_dispalyer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import Tuple, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .render.hexapod_leg_power import HexapodLegPower
from .calc.hexapod_leg_range_calculator import HexapodLegRangeCalculator
from .calc.hexapod_param_protocol import HexapodParamProtocol
from .render.approximated_graph_renderer import ApproximatedGraphRenderer
from .render.color_param import ColorParam
from .render.display_flag import DisplayFlag
from .render.hexapod_leg_renderer import HexapodLegRenderer
from .render.hexapod_range_of_motion_renderer import HexapodRangeOfMotionRenderer
from .render.mouse_grid_renderer import MouseGridRenderer

mpl.use("tkagg")


class GraphDisplayer:
    """
    グラフを表示するクラス．
    """

    def display(
        self,
        hexapod_pram : HexapodParamProtocol,
        *,
        rect: Tuple[float, float, float, float] = (-100.0, 300.0, -200.0, 200.0),
        display_flag: DisplayFlag = DisplayFlag(),
        color_param: ColorParam = ColorParam(),
        leg_power_step: float =2.0,
        image_file_name: str="result/img_main.png",
        ground_z: float =-25.0,
        do_not_show: bool =False,
        figure : Optional[Figure] = None,
        axes: Optional[Axes] = None,
        axes_table: Optional[Axes] = None,
    ):
        """
        x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画する．\n
        変数の値を変更することで処理の内容を変更できる．
        """

        if display_flag.display_table:
            if figure is None or axes is None or axes_table is None:
                fig = plt.figure()  # type: ignore
                ax = fig.add_subplot(1, 2, 1)  # type: ignore
                ax_table = fig.add_subplot(1, 2, 2)  # type: ignore
            else:
                fig = figure
                ax = axes
                ax_table = axes_table
        else:
            if figure is None or axes is None:
                fig = plt.figure()  # type: ignore
                ax = fig.add_subplot(1, 1, 1)  # type: ignore
                # 今回は使用しないので適当な座標に配置.
                ax_table = fig.add_subplot(3, 3, 2)  # type: ignore
                ax_table.set_visible(False)  # 表示しない.
            else:
                fig = figure
                ax = axes
                ax_table = None

        # 以下グラフの作成，描画.
        hexapod_calc = HexapodLegRangeCalculator(hexapod_pram)

        # 脚が出せる力のグラフを描画.
        hexapod_leg_power = HexapodLegPower(
            hexapod_calc, hexapod_pram, fig, ax,
            rect=rect,
            step=leg_power_step,
        )

        if display_flag.display_leg_power:
            hexapod_leg_power.render()

        # 脚の可動範囲の近似値を描画.
        app_graph = ApproximatedGraphRenderer(
            hexapod_pram,
            ax,
            color_param= color_param,
            display_flag= display_flag,
            z_min_max=(rect[2], rect[3])
        )

        if display_flag.display_approximated_graph:
            app_graph.render()

        # 脚を描画.
        leg_renderer = HexapodLegRenderer(
            hexapod_pram, fig, ax, ax_table,
            color_param= color_param,
            display_flag= display_flag
        )
        leg_renderer.set_img_file_name(image_file_name)
        leg_renderer.render()

        # マウスがグラフのどこをポイントしているかを示す線を描画する.
        mouse_grid_renderer = MouseGridRenderer(fig, ax, color_param= color_param)
        if display_flag.display_mouse_grid:
            mouse_grid_renderer.render()

        # 脚の可動範囲を描画する.
        hexapod_range_of_motion = HexapodRangeOfMotionRenderer(
            hexapod_pram,
            fig,
            ax,
            color_param= color_param
        )
        hexapod_range_of_motion.render()

        ax.set_xlim(rect[0], rect[1])  # x 軸の範囲を設定.
        ax.set_ylim(rect[2], rect[3])  # z 軸の範囲を設定.

        ax.set_xlabel("x [mm]")  # type: ignore
        ax.set_ylabel("z [mm]")  # type: ignore

        ax.set_aspect("equal")  # x,y軸のスケールを揃える.

        if display_flag.display_ground_line:
            ax.plot([rect[0], rect[1]], [ground_z, ground_z])  # type: ignore

        if not do_not_show:
            plt.show()  # type: ignore
