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
    """a class to draw a grid on the mouse point"""

    def __init__(
        self,
        fig: Figure,
        ax: Axes,
        *,
        color_param: ColorParam = ColorParam(),
    ) -> None:
        self._alreadly_init: bool = False

        self._fig = fig
        self._ax = ax
        self._x_axis: Line2D = self._ax.axhline(-1)  # type: ignore
        self._x_axis.set_linestyle("--")
        self._y_axis: Line2D = self._ax.axvline(-1)  # type: ignore
        self._y_axis.set_linestyle("--")

        self._color_param = color_param

    def render(self) -> None:
        """
        event is set, the second and subsequent calls are ignored.\n
        If you display a matplotlib figure object after calling this
        function, a line will be displayed to show the mouse point.
        a line is displayed to show the mouse point.\n
        must be called before plt.show() or plt.draw()
        must be called after this function.
        """

        print(f"{__name__}: Starts drawing the mouse grid")
        print(f"{__name__}: {self._color_param.mouse_grid_color=}")
        print(f"{__name__}: {self._color_param.mouse_grid_alpha=}")

        if self._alreadly_init:
            print(f"{__name__}: Already initialized.")
            return

        self._y_axis.set_alpha(self._color_param.mouse_grid_alpha)
        self._x_axis.set_alpha(self._color_param.mouse_grid_alpha)

        self._y_axis.set_color(self._color_param.mouse_grid_color)
        self._x_axis.set_color(self._color_param.mouse_grid_color)

        # Set functions to update the x and y axis lines when the mouse moves
        self._fig.canvas.mpl_connect("motion_notify_event", self._on_move)

        self._alreadly_init = True

    def _on_move(self, event: Event) -> None:
        if not isinstance(event, MouseEvent):
            return
        x = event.xdata
        y = event.ydata
        if x is None or y is None:
            return
        # Update the x and y axis lines to the mouse position
        self._y_axis.set_xdata([float(x)])
        self._x_axis.set_ydata([float(y)])
