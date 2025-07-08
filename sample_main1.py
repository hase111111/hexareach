"""
sample_main1.py
This is a sample code to display the phantom X graph.
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


import hexareach as hxr


if __name__ == "__main__":
    # Display the phantom X graph.
    graph = hxr.GraphDisplayer()

    graph.display(hxr.PhantomxMk2Param())
