"""
sample_main4.py
グラフに点や線を追加してから表示するサンプル.
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

    # グラフを表示する前に, 点を追加
    ax.plot([0, 50, 100, 150, 200], [0, 50, 100, 150, 200], "rx")  # type: ignore[no-untyped-call]

    # グラフを表示する前に, 線を追加
    ax.plot([0, 200], [0, -200], "b-")  # type: ignore[no-untyped-call]

    # グラフを表示
    graph.display(
        hxr.PhantomxMk2Param(),
        display_flag=flag,
        figure=fig,
        axes=ax)
