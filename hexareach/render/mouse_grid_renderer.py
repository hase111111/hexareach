"""
mouse_grid_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import matplotlib.axes as axes
import matplotlib.pyplot as plt


class MouseGridRenderer:
    """a class to draw a grid on the mouse point"""

    def __init__(
        self,
        fig: plt.Figure,
        ax: axes.Axes,
        *,
        alpha: float = 0.5,
        color: str = "black"
    ) -> None:
        self._alreadly_init: bool = False

        self._fig = fig
        self._ax = ax

        if self._fig is None:
            raise ValueError(f"{__name__}: fig is None")

        if self._ax is None:
            raise ValueError(f"{__name__}: ax is None")

        self._x_axis = self._ax.axhline(-1)
        self._x_axis.set_linestyle("--")
        self._y_axis = self._ax.axvline(-1)
        self._y_axis.set_linestyle("--")

        self.set_alpha(alpha)
        self.set_color(color)

    def render(self) -> None:
        """
        イベントを設定する,2度目以降の呼び出しは無視される．\n
        この関数を呼んだ後に matplotlib の figure オブジェクトを表示すると,
        マウスポイント地点を表示するための線が表示される．\n
        plt.show() の前に呼び出す, またはこの関数の後に plt.draw() を呼び出す必要がある．
        """

        print(f"{__name__}: Starts drawing the mouse grid")
        print(f"{__name__}: alpha: {self._alpha}, color: {self._color}")

        if self._alreadly_init:
            print(f"{__name__}: Already initialized.")
            return

        self._y_axis.set_alpha(self._alpha)
        self._x_axis.set_alpha(self._alpha)

        self._y_axis.set_color(self._color)
        self._x_axis.set_color(self._color)

        # マウスが動いたときに呼び出す関数を設定
        self._fig.canvas.mpl_connect("motion_notify_event", self._on_move)

        self._alreadly_init = True

        return

    def _on_move(self, event) -> None:
        # マウスポイント地点を取得
        x = event.xdata
        y = event.ydata

        if x is None or y is None:
            # マウスポイント地点が取得できなかった場合は何もしない．
            return

        # マウスポイント地点を表示するための線の位置を更新．
        self._y_axis.set_xdata([float(x)])
        self._x_axis.set_ydata([float(y)])

    def set_alpha(self, alpha: float) -> None:
        """
        マウスポイント地点を表示するための線の透明度を設定する．\n
        set_event()の前にを呼び出す必要がある．

        Parameters
        ----------
        alpha : float
            透明度 (0.0 ~ 1.0)
        """

        self._alpha = alpha

        # clamp alpha to 0.0 ~ 1.0
        if self._alpha < 0.0:
            self._alpha = 0.0
        elif self._alpha > 1.0:
            self._alpha = 1.0

    def set_color(self, color: str) -> None:
        """
        マウスポイント地点を表示するための線の色を設定する．\n
        描画の前にを呼び出す必要がある．

        Parameters
        ----------
        color : str
            色
        """

        self._color = color
