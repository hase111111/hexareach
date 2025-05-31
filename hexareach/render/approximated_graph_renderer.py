"""
approximated_graph_renderer.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from typing import Tuple

from matplotlib import axes
import numpy as np

from .color_param import ColorParam
from ..hexapod_leg_range_calculator import HexapodLegRangeCalculator
from ..hexapod_param import HexapodParamProtocol


class ApproximatedGraphRenderer:
    """
    A class that renders the approximated leg range of motion graph.
    This class uses the HexapodLegRangeCalculator to calculate the
    approximated leg range of motion and renders it on the given axes.
    """

    def __init__(
        self,
        hexapod_param: HexapodParamProtocol,
        ax: axes.Axes,
        *,
        color_param: ColorParam = ColorParam(),
        z_min_max: Tuple[float, float] = (-300.0, 300.0)
    ) -> None:
        self._calc = HexapodLegRangeCalculator(hexapod_param)
        self._ax = ax
        self._color_param = color_param
        self._graph_step = 0.01
        self.set_range(
            z_min=z_min_max[0],
            z_max=z_min_max[1]
        )

    def render(self) -> None:
        """
        Display the Approximated leg range of motion.
        The set function must be called before this function.
        """

        print(f"{__name__}: Shows approximate leg range of motion")

        color = self._color_param.approximated_graph_color
        alpha = self._color_param.approximated_graph_alpha
        draw_fill = self._color_param.approximated_graph_filled

        # Calculate the range of motion of the approximated leg.
        # Create an array z from z_min to z_max in graph_step ticks.
        z = np.arange(self._z_min, self._z_max, self._graph_step)

        # Create an array z with the same number of
        # elements as x and all min_leg_radius values.
        approximated_x_min = np.full_like(
            z, self._calc.get_approximate_min_leg_raudus()
        )

        # Create an empty np array.
        approximated_x_max = np.empty([0])

        for _, z_value in enumerate(z):
            approximated_x_max = np.append(
                approximated_x_max,
                self._calc.get_approximate_max_leg_raudus(z_value),
            )

        # Fill the area enclosed by x and z.
        if draw_fill:
            self._ax.fill_betweenx(  # type: ignore
                z,
                approximated_x_min,
                approximated_x_max,
                where=(approximated_x_max >= approximated_x_min).tolist(),
                color=color,
                alpha=alpha,
            )
        else:
            self._ax.plot(  # type: ignore
                approximated_x_min, z, color=color, alpha=alpha)
            self._ax.plot(  # type: ignore
                approximated_x_max, z, color=color, alpha=alpha)

    def set_range(self, z_min: float, z_max: float) -> None:
        """
        Sets the range of the range of motion of the approximated leg.

        Parameters
        ----------
        z_min : float
            z minimum value.
        z_max : float
            z maximum value.

        Raises
        ------
        ValueError
            If z_min is greater than z_max.
        """

        self._z_min = z_min
        self._z_max = z_max

        # Check if z_min is less than or equal to z_max
        if self._z_min > self._z_max:
            raise ValueError(f"{__name__}: {z_min=} is greater than {z_max=}")
