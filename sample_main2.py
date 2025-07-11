"""
sample_main2.py
脚先が出すことができる力を計算するサンプルプログラム.
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import hexareach as hxr


if __name__ == "__main__":
    graph = hxr.GraphDisplayer()

    # DisplayFlag の display_leg_power を True にすることで
    # 力の計算を行って描画することができます.
    flag = hxr.DisplayFlag()
    flag.display_leg_power = True
    flag.display_table = False
    flag.leg_circle_displayed = False
    flag.leg_wedge_displayed = False

    graph.display(
        hxr.PhantomxMk2Param(),
        display_flag=flag,
        leg_power_step=5.0,
        image_file_name="result/sample_main2.png",
    )
