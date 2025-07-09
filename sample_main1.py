"""
sample_main1.py
PhantomX Mk-2 の脚の可動範囲を計算する基本的なサンプルプログラム.
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


import hexareach as hxr


if __name__ == "__main__":
    # Display the phantom X graph.
    graph = hxr.GraphDisplayer()

    graph.display(hxr.PhantomxMk2Param())
