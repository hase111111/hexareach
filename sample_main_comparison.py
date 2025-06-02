# -*- coding: utf-8 -*-

# Copyright (c) 2023 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

# Sample code to change robot conditions and display graphs

import math

import hexareach as hr


if __name__ == "__main__":
    param1 = hr.HexapodParam()
    graph1 = hr.GraphDisplayer()

    fig, ax1, ax2 = graph1.display(
        # set display options
        display_table=False,
        display_approximated_graph=False,
        display_ground_line=False,
        display_mouse_grid=False,
        # set file name to save the image
        image_file_name="result/sample_main4.png",
        x_min=-150.0,
        x_max=350.0,
        z_min=-250.0,
        z_max=250,
        # do not display the graph
        do_not_show=True,
    )
    param = hr.HexapodParam()

    # Change the robot conditions.
    param.coxa_length = 45.0
    param.femur_length = 75.0
    param.tibia_length = 140.0

    param.theta2_max = math.radians(90.0)
    param.theta2_min = math.radians(-90.0)

    param.theta3_max = math.radians(0.0)
    param.theta3_min = math.radians(-170.0)

    # param.torque_max = 3700.0

    # Display the phantom cross graph.
    graph = hr.GraphDisplayer()

    graph.display(
        # use the changed robot conditions.
        param,
        # set display options.
        display_table=False,
        display_approximated_graph=False,
        display_ground_line=False,
        ground_z=-30.0,
        display_mouse_grid=False,
        # display_leg_power=True,
        # leg_power_step=5.0,
        # set display range.
        x_min=-150.0,
        x_max=350.0,
        z_min=-250.0,
        z_max=250,
        # set file name to save the image.
        image_file_name="sample_main_ex.png",
    )
