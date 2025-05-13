"""graph_dispalyer.py"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import Tuple

# モジュールのインポート
import matplotlib as mpl

mpl.use("tkagg")
import matplotlib.axes as axes
import matplotlib.pyplot as plt

from .hexapod_leg_power import HexapodLegPower
from .hexapod_leg_range_calculator import HexapodLegRangeCalculator
from .approximated_graph_renderer import ApproximatedGraphRenderer
from .hexapod_leg_renderer import HexapodLegRenderer
from .render.mouse_grid_renderer import MouseGridRenderer
from .hexapod_range_of_motion import HexapodRangeOfMotion
from .hexapod_param import HexapodParam


class GraphDisplayer:

    def display(
        self,
        hexapod_pram=HexapodParam(),
        *,
        display_table=True,
        display_leg_power=False,
        display_approximated_graph=True,
        display_mouse_grid=True,
        display_ground_line=True,
        display_circle=True,
        display_wedge=True,
        x_min=-100.0,
        x_max=300.0,
        z_min=-200.0,
        z_max=200.0,
        leg_power_step=2.0,
        approx_fill=True,
        color_approx="green",
        alpha_approx=0.5,
        color_rom="black",
        alpha_upper_rom=0.3,
        alpha_lower_rom=1.0,
        color_mouse_grid="black",
        alpha_mouse_grid=0.5,
        image_file_name="result/img_main.png",
        ground_z=-25.0,
        do_not_show=False
    ) -> Tuple[plt.Figure, axes.Axes, axes.Axes]:
        """
        x_min < x < x_max , z_min < z < z_max の範囲でグラフを描画する．\n
        変数の値を変更することで処理の内容を変更できる．

        Parameters
        ----------
        display_table: bool
            表を表示するか．
        display_leg_power: bool
            脚が出せる力のグラフを表示するか．
        display_approximated_graph: bool
            脚の可動範囲の近似値を表示するか．
        display_circle: bool
            脚の可動域を円で表示するか．
        display_wedge: bool
            可動範囲を扇形で表示するか．
        display_ground_line: bool
            地面の線を表示するか．
        display_mouse_grid: bool
            マウスがグラフのどこをポイントしているかを示す線を表示するか．
        x_min: float
            x軸の最小値．
        x_max: float
            x軸の最大値．
        z_min: float
            z軸の最小値．
        z_max: float
            z軸の最大値．
        leg_power_step: float
            何mmごとに力の分布を計算するか．
        approx_fill: bool
            脚の可動範囲の近似値を塗りつぶすかどうか．
        color_approx: str
            脚の可動範囲の近似値の色．
        alpha_approx: float
            脚の可動範囲の近似値の透明度．
        color_rom: str
            脚の可動範囲の色．
        alpha_upper_rom: float
            脚の可動範囲の上側の透明度．
        alpha_lower_rom: float
            脚の可動範囲の下側の透明度．
        color_mouse_grid: str
            マウスがグラフのどこをポイントしているかを示す線の色．
        alpha_mouse_grid: float
            マウスがグラフのどこをポイントしているかを示す線の透明度．
        image_file_name: str
            脚を画像で表示する場合の画像ファイル名.
        ground_z: float
            地面の高さ．
        do_not_show: bool
            show()を実行しない場合にTrueにする．

        Returns
        -------
        fig : matplotlib.figure.Figure
            グラフのfigureオブジェクト．
        ax : matplotlib.axes.Axes
            グラフのaxesオブジェクト．
        ax_table : matplotlib.axes.Axes
            表のaxesオブジェクト．
        """

        X_MIN = x_min
        X_MAX = x_max
        Z_MIN = z_min
        Z_MAX = z_max

        if display_table:
            self._fig = plt.figure()
            self._ax = self._fig.add_subplot(1, 2, 1)
            self._ax_table = self._fig.add_subplot(1, 2, 2)
        else:
            self._fig = plt.figure()
            self._ax = self._fig.add_subplot(1, 1, 1)
            self._ax_table = self._fig.add_subplot(
                3, 3, 2
            )  # 今回は使用しないので適当な座標に配置.
            self._ax_table.set_visible(False)  # 表示しない.

        # 以下グラフの作成，描画.
        hexapod_calc = HexapodLegRangeCalculator(hexapod_pram)

        # 脚が出せる力のグラフを描画.
        hexapod_leg_power = HexapodLegPower(
            hexapod_calc,
            hexapod_pram,
            self._fig,
            self._ax,
            x_min=X_MIN,
            x_max=X_MAX,
            z_min=Z_MIN,
            z_max=Z_MAX,
            step=leg_power_step,
        )

        if display_leg_power:
            hexapod_leg_power.render()

        # 脚の可動範囲の近似値を描画.
        app_graph = ApproximatedGraphRenderer(
            hexapod_calc,
            self._ax,
            z_min=Z_MIN,
            z_max=Z_MAX,
            draw_additional_line=True,
            draw_fill=approx_fill,
            color=color_approx,
            alpha=alpha_approx,
        )

        if display_approximated_graph:
            app_graph.render()

        # 脚を描画.
        self.leg_renderer = HexapodLegRenderer(
            hexapod_calc,
            hexapod_pram,
            self._fig,
            self._ax,
            self._ax_table,
            display_circle=display_circle,
            display_wedge=display_wedge,
        )
        self.leg_renderer.set_img_file_name(image_file_name)
        self.leg_renderer.render()

        # マウスがグラフのどこをポイントしているかを示す線を描画する.
        self.mouse_grid_renderer = MouseGridRenderer(
            self._fig, self._ax, alpha=alpha_mouse_grid, color=color_mouse_grid
        )
        if display_mouse_grid:
            self.mouse_grid_renderer.render()

        # 脚の可動範囲を描画する.
        hexapod_range_of_motion = HexapodRangeOfMotion(
            hexapod_calc,
            hexapod_pram,
            self._ax,
            color=color_rom,
            upper_alpha=alpha_upper_rom,
            lowwer_alpha=alpha_lower_rom,
        )
        hexapod_range_of_motion.render()

        self._ax.set_xlim(X_MIN, X_MAX)  # x 軸の範囲を設定.
        self._ax.set_ylim(Z_MIN, Z_MAX)  # z 軸の範囲を設定.

        self._ax.set_xlabel("x [mm]")  # x軸のラベルを設定.
        self._ax.set_ylabel("z [mm]")  # y軸のラベルを設定.

        self._ax.set_aspect("equal")  # x,y軸のスケールを揃える.

        if display_ground_line:
            self._ax.plot([X_MIN, X_MAX], [ground_z, ground_z])  # グラフを描画する.

        if not do_not_show:
            plt.show()  # 表示する.

        return self._fig, self._ax, self._ax_table
