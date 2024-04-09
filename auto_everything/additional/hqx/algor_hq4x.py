#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
The hq4x algorithm. Outputs a 4x4 grid.
"""
import auto_everything.additional.hqx.interpolate as interpolate
import auto_everything.additional.hqx.rgb_yuv as rgb_yuv
import auto_everything.additional.hqx.constants as constants

# Local binding to squeeze some performance (and bytes)
mix_3_to_1 = interpolate.mix_3_to_1
mix_2_to_1_to_1 = interpolate.mix_2_to_1_to_1
mix_4_to_2_to_1 = interpolate.mix_4_to_2_to_1
mix_6_to_1_to_1 = interpolate.mix_6_to_1_to_1
mix_7_to_1 = interpolate.mix_7_to_1
mix_even = interpolate.mix_even
mix_5_to_3 = interpolate.mix_5_to_3
yuv_equal = rgb_yuv.yuv_equal

# Context positionings
TOP_LEFT = constants.TOP_LEFT
TOP = constants.TOP
TOP_RIGHT = constants.TOP_RIGHT
LEFT = constants.LEFT
CENTER = constants.CENTER
RIGHT = constants.RIGHT
BOTTOM_LEFT = constants.BOTTOM_LEFT
BOTTOM = constants.BOTTOM
BOTTOM_RIGHT = constants.BOTTOM_RIGHT

# Output grid positions, 16x16:
# T for top, B for bottom, L for left, R for right.
# First letter is vertical halves of the grid
# Second letter is for the horizontal halves of the above vertical halves
# Third letter is for which vertical half of the 2x2 selection
# Fourth letter is for which 2x1 element out of the above divided selection

# ╔════╦════╦════╦════╗
# ║ 0  ║ 1  ║ 2  ║ 3  ║ TOP VERTICAL
# ╠════╬════╬════╬════╣
# ║ 4  ║ 5  ║ 6  ║ 7  ║ TOP VERTICAL
# ╠════╬════╬════╬════╣
# ║ 8  ║ 9  ║ 10 ║ 11 ║ BOTTOM VERTICAL
# ╠════╬════╬════╬════╣
# ║ 12 ║ 13 ║ 14 ║ 15 ║ BOTTOM VERTICAL
# ╚════╩════╩════╩════╝
#   LEFT    |  RIGHT
# T R B L -> Top half, right side, bottom half, left corner = 6.
OUT_T_L_T_L = 0
OUT_T_L_T_R = 1
OUT_T_R_T_L = 2
OUT_T_R_T_R = 3
OUT_T_L_B_L = 4
OUT_T_L_B_R = 5
OUT_T_R_B_L = 6
OUT_T_R_B_R = 7
OUT_B_L_T_L = 8
OUT_B_L_T_R = 9
OUT_B_R_T_L = 10
OUT_B_R_T_R = 11
OUT_B_L_B_L = 12
OUT_B_L_B_R = 13
OUT_B_R_B_L = 14
OUT_B_R_B_R = 15


def hq4x_pixel(context: list[int]) -> list[int]:
    """
    Output a 16 integer list (4x4) of the 4x scaled `context`.

    :param context: A 9 integer list of the center and surrounding pixel equalities.
    :return: A 16 integer list (4x4).
    """
    yuv_context = [rgb_yuv.rgb_int_to_yuv_int(rgb) for rgb in context]
    pattern = interpolate.generate_pattern(context, yuv_context)

    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if pattern in (0, 1, 4, 32, 128, 5, 132, 160, 33, 129, 36, 133, 164, 161, 37, 165):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (2, 34, 130, 162):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (16, 17, 48, 49):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (64, 65, 68, 69):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (8, 12, 136, 140):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (3, 35, 131, 163):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (6, 38, 134, 166):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (20, 21, 52, 53):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (144, 145, 176, 177):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
    elif pattern in (192, 193, 196, 197):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (96, 97, 100, 101):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (40, 44, 168, 172):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (9, 13, 137, 141):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (18, 50):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (80, 81):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (72, 76):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (10, 138):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 66:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 24:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (7, 39, 135):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (148, 149, 180):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
    elif pattern in (224, 228, 225):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
    elif pattern in (41, 169, 45):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (22, 54):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (208, 209):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (104, 108):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (11, 139):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (19, 51):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_T_R] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_L] = mix_5_to_3(context[TOP], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[TOP])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (146, 178):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_R_T_L] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_5_to_3(context[RIGHT], context[TOP])
            result[OUT_B_R_T_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern in (84, 85):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_5_to_3(context[RIGHT], context[BOTTOM])
            result[OUT_B_R_B_L] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (112, 113):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_R] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_L] = mix_5_to_3(context[BOTTOM], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern in (200, 204):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        else:
            result[OUT_B_L_T_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_5_to_3(context[BOTTOM], context[LEFT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (73, 77):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_T_L] = mix_5_to_3(context[LEFT], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[LEFT])

        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (42, 170):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_5_to_3(context[LEFT], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_B_L_T_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (14, 142):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_5_to_3(context[TOP], context[LEFT])
            result[OUT_T_R_T_L] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])

        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 67:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 70:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 28:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 152:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
    elif pattern == 194:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
    elif pattern == 98:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 56:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 25:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (26, 31):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (82, 214):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (88, 248):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern in (74, 107):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 27:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 86:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 216:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 106:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 30:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 210:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 120:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 75:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 29:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 198:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 184:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 99:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 57:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 71:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 156:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 226:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 60:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 195:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 102:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 153:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 58:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 83:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 92:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 202:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 78:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 154:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 114:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])

    elif pattern == 89:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 90:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (55, 23):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_T_R] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_L] = mix_5_to_3(context[TOP], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[TOP])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (182, 150):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
            result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_R_T_L] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_5_to_3(context[RIGHT], context[TOP])
            result[OUT_B_R_T_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern in (213, 212):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_5_to_3(context[RIGHT], context[BOTTOM])
            result[OUT_B_R_B_L] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (241, 240):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_R] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_L] = mix_5_to_3(context[BOTTOM], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern in (236, 232):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
            result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        else:
            result[OUT_B_L_T_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_5_to_3(context[BOTTOM], context[LEFT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (109, 105):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_T_L] = mix_5_to_3(context[LEFT], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[LEFT])

        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (171, 43):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
            result[OUT_T_L_B_R] = context[CENTER]
            result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_5_to_3(context[LEFT], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_B_L_T_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (143, 15):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
            result[OUT_T_L_B_L] = context[CENTER]
            result[OUT_T_L_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_5_to_3(context[TOP], context[LEFT])
            result[OUT_T_R_T_L] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])

        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 124:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 203:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 62:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 211:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 118:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 217:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 110:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 155:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 188:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 185:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 61:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 157:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 103:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 227:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 230:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 199:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 220:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern == 158:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 234:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 242:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])

    elif pattern == 59:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 121:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 87:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 79:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 122:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 94:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 218:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern == 91:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_R] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 229:
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 167:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 173:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 181:
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 186:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 115:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])

    elif pattern == 93:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 206:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (205, 201):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (174, 46):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_R] = context[CENTER]

        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (179, 147):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern in (117, 116):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])

    elif pattern == 189:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 231:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 126:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 219:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 125:
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_T_L] = mix_5_to_3(context[LEFT], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[LEFT])

        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 221:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
            result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_B_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_5_to_3(context[RIGHT], context[BOTTOM])
            result[OUT_B_R_B_L] = mix_2_to_1_to_1(context[BOTTOM], context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 207:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
            result[OUT_T_L_B_L] = context[CENTER]
            result[OUT_T_L_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_5_to_3(context[TOP], context[LEFT])
            result[OUT_T_R_T_L] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_B_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])

        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 238:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
            result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        else:
            result[OUT_B_L_T_L] = mix_2_to_1_to_1(context[LEFT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_5_to_3(context[BOTTOM], context[LEFT])
            result[OUT_B_R_B_L] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM])

        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 190:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
            result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_R_T_L] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_5_to_3(context[RIGHT], context[TOP])
            result[OUT_B_R_T_R] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_R] = mix_3_to_1(context[CENTER], context[RIGHT])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 187:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
            result[OUT_T_L_B_R] = context[CENTER]
            result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_2_to_1_to_1(context[TOP], context[CENTER], context[LEFT])
            result[OUT_T_L_B_L] = mix_5_to_3(context[LEFT], context[TOP])
            result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_B_L_T_L] = mix_3_to_1(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[LEFT])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 243:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_L] = context[CENTER]
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
            result[OUT_B_R_T_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[OUT_B_L_B_R] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_L] = mix_5_to_3(context[BOTTOM], context[RIGHT])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern == 119:
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
            result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_L] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_T_L_T_R] = mix_3_to_1(context[TOP], context[CENTER])
            result[OUT_T_R_T_L] = mix_5_to_3(context[TOP], context[RIGHT])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_T_R_B_R] = mix_2_to_1_to_1(context[RIGHT], context[CENTER], context[TOP])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (237, 233):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern in (175, 47):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
        result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern in (183, 151):
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern in (245, 244):
        result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_L_B_R] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 250:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

    elif pattern == 123:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 95:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 222:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 252:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_LEFT])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 249:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]

    elif pattern == 235:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 111:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 63:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 159:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[BOTTOM_LEFT])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 215:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 246:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 254:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_T_R] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 253:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_L] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP])
        result[OUT_T_L_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_T_R_B_R] = mix_7_to_1(context[CENTER], context[TOP])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 251:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_T_R_B_R] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]

    elif pattern == 239:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        result[OUT_T_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_T_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_T_R] = mix_5_to_3(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]
        result[OUT_B_R_B_L] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[RIGHT])

    elif pattern == 127:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_L] = context[CENTER]
            result[OUT_T_R_T_R] = context[CENTER]
            result[OUT_T_R_B_R] = context[CENTER]
        else:
            result[OUT_T_R_T_L] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_R_T_R] = mix_even(context[TOP], context[RIGHT])
            result[OUT_T_R_B_R] = mix_even(context[RIGHT], context[CENTER])

        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_T_L] = context[CENTER]
            result[OUT_B_L_B_L] = context[CENTER]
            result[OUT_B_L_B_R] = context[CENTER]
        else:
            result[OUT_B_L_T_L] = mix_even(context[LEFT], context[CENTER])
            result[OUT_B_L_B_L] = mix_even(context[BOTTOM], context[LEFT])
            result[OUT_B_L_B_R] = mix_even(context[BOTTOM], context[CENTER])

        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_T_R] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_L] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 191:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_L] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_R_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_L_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM])
        result[OUT_B_R_B_R] = mix_5_to_3(context[CENTER], context[BOTTOM])

    elif pattern == 223:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
            result[OUT_T_L_T_R] = context[CENTER]
            result[OUT_T_L_B_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_even(context[TOP], context[LEFT])
            result[OUT_T_L_T_R] = mix_even(context[TOP], context[CENTER])
            result[OUT_T_L_B_L] = mix_even(context[LEFT], context[CENTER])

        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_T_R] = context[CENTER]
            result[OUT_B_R_B_L] = context[CENTER]
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_T_R] = mix_even(context[RIGHT], context[CENTER])
            result[OUT_B_R_B_L] = mix_even(context[BOTTOM], context[CENTER])
            result[OUT_B_R_B_R] = mix_even(context[BOTTOM], context[RIGHT])

        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_B_L_B_R] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 247:
        result[OUT_T_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_T_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_T_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        result[OUT_B_L_B_L] = mix_5_to_3(context[CENTER], context[LEFT])
        result[OUT_B_L_B_R] = mix_7_to_1(context[CENTER], context[LEFT])
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    elif pattern == 255:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_T_L_T_L] = context[CENTER]
        else:
            result[OUT_T_L_T_L] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[LEFT])

        result[OUT_T_L_T_R] = context[CENTER]
        result[OUT_T_R_T_L] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_T_R_T_R] = context[CENTER]
        else:
            result[OUT_T_R_T_R] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])

        result[OUT_T_L_B_L] = context[CENTER]
        result[OUT_T_L_B_R] = context[CENTER]
        result[OUT_T_R_B_L] = context[CENTER]
        result[OUT_T_R_B_R] = context[CENTER]
        result[OUT_B_L_T_L] = context[CENTER]
        result[OUT_B_L_T_R] = context[CENTER]
        result[OUT_B_R_T_L] = context[CENTER]
        result[OUT_B_R_T_R] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_B_L_B_L] = context[CENTER]
        else:
            result[OUT_B_L_B_L] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])

        result[OUT_B_L_B_R] = context[CENTER]
        result[OUT_B_R_B_L] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_B_R_B_R] = context[CENTER]
        else:
            result[OUT_B_R_B_R] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[RIGHT])

    return result
