"""
sample_main4.py
Sample code for adding dots and lines to a graph
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import matplotlib.pyplot as plt

import hexareach as hxr


if __name__ == "__main__":
    # 通常通り, matplotlib の Fig を追加
    fig = plt.figure()  # type: ignore
    ax = fig.add_subplot(1, 1, 1)  # type: ignore

    graph = hxr.GraphDisplayer()
    flag = hxr.DisplayFlag()
    flag.display_table = False

    # Add sample points.
    ax.plot([0, 50, 100, 150, 200], [0, 50, 100, 150, 200], "rx")  # type: ignore[no-untyped-call]

    # Add a line.
    ax.plot([0, 200], [0, -200], "b-")  # type: ignore[no-untyped-call]

    graph.display(
        hxr.PhantomxMk2Param(),
        display_flag=flag,
        figure=fig,
        axes=ax)
