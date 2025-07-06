"""
mouse_grid_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backend_bases import Event, MouseEvent

from .color_param import ColorParam

class MouseGridRenderer:
    """
    マウス位置にグリッド線を描画するクラス
    """

    def __init__(
        self,
        fig: Figure,
        ax: Axes,
        *,
        color_param: ColorParam = ColorParam(),
    ) -> None:
        """
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            描画対象のFigureオブジェクト
        ax : matplotlib.axes.Axes
            描画対象のAxesオブジェクト
        color_param : ColorParam, optional
            グリッド線の色や透明度のパラメータ
        """
        # 初期化済みかどうかのフラグ
        self._alreadly_init: bool = False

        self._fig = fig
        self._ax = ax
        # マウス位置に合わせて動く水平線を初期化
        self._x_axis: Line2D = self._ax.axhline(-1)  # type: ignore
        self._x_axis.set_linestyle("--")
        # マウス位置に合わせて動く垂直線を初期化
        self._y_axis: Line2D = self._ax.axvline(-1)  # type: ignore
        self._y_axis.set_linestyle("--")

        self._color_param = color_param

    def render(self) -> None:
        """
        マウス位置グリッドの描画イベントをセットする（2回目以降は無視）
        この関数を呼び出した後にmatplotlibのfigureを表示すると、
        マウス位置に応じて線が表示される。
        plt.show()やplt.draw()の前に呼び出す必要がある。
        """

        print(f"{__name__}: Starts drawing the mouse grid")
        print(f"{__name__}: {self._color_param.mouse_grid_color = }")
        print(f"{__name__}: {self._color_param.mouse_grid_alpha = }")

        if self._alreadly_init:
            print(f"{__name__}: Already initialized.")
            return

        # 線の透明度を設定
        self._y_axis.set_alpha(self._color_param.mouse_grid_alpha)
        self._x_axis.set_alpha(self._color_param.mouse_grid_alpha)

        # 線の色を設定
        self._y_axis.set_color(self._color_param.mouse_grid_color)
        self._x_axis.set_color(self._color_param.mouse_grid_color)

        # マウス移動時に線を更新する関数を登録
        self._fig.canvas.mpl_connect("motion_notify_event", self._on_move)

        self._alreadly_init = True

    def _on_move(self, event: Event) -> None:
        # MouseEventでなければ何もしない
        if not isinstance(event, MouseEvent):
            return
        x = event.xdata
        y = event.ydata
        if x is None or y is None:
            return
        # マウス位置にグリッド線を移動
        self._y_axis.set_xdata([float(x)])
        self._x_axis.set_ydata([float(y)])
