"""
sample_main4.py
Sample code for adding dots and lines to a graph
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import matplotlib.pyplot as plt

import phantom_cross as pc


if __name__ == "__main__":
    graph = pc.GraphDisplayer()

    fig, ax1, ax2 = graph.display(
        # set display options
        display_table=False,
        display_circle=False,
        display_wedge=False,
        display_approximated_graph=False,
        display_ground_line=False,
        # set file name to save the image
        image_file_name="result/sample_main4.png",
        # do not display the graph
        do_not_show=True,
    )

    # Add sample points.
    ax1.plot([0, 50, 100, 150, 200], [0, 50, 100, 150, 200], "rx")

    # Add a line.
    ax1.plot([0, 200], [0, -200], "b-")

    # Show the graph.
    plt.show()
