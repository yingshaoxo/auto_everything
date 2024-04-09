#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
The hq3x algorithm. Outputs a 3x3 grid.
"""
import auto_everything.additional.hqx.interpolate as interpolate
import auto_everything.additional.hqx.rgb_yuv as rgb_yuv
import auto_everything.additional.hqx.constants as constants

# Local binding to squeeze some performance (and bytes)
mix_3_to_1 = interpolate.mix_3_to_1
mix_2_to_1_to_1 = interpolate.mix_2_to_1_to_1
mix_2_to_7_to_7 = interpolate.mix_2_to_7_to_7
mix_7_to_1 = interpolate.mix_7_to_1
mix_even = interpolate.mix_even
yuv_equal = rgb_yuv.yuv_equal

# Context positions
TOP_LEFT = constants.TOP_LEFT
TOP = constants.TOP
TOP_RIGHT = constants.TOP_RIGHT
LEFT = constants.LEFT
CENTER = constants.CENTER
RIGHT = constants.RIGHT
BOTTOM_LEFT = constants.BOTTOM_LEFT
BOTTOM = constants.BOTTOM
BOTTOM_RIGHT = constants.BOTTOM_RIGHT

# Output grid is the same as above, 3x3


def hq3x_pixel(context: list[int]) -> list[int]:
    """
    Output a 9 integer list (3x3) of the 3x scaled `context`.

    :param context: A 9 integer list of the center and surrounding pixel equalities.
    :return: A 9 integer list (3x3).
    """
    yuv_context = [rgb_yuv.rgb_int_to_yuv_int(rgb) for rgb in context]
    pattern = interpolate.generate_pattern(context, yuv_context)

    result = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if pattern in (0, 1, 4, 32, 128, 5, 132, 160, 33, 129, 36, 133, 164, 161, 37, 165):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (2, 34, 130, 162):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (16, 17, 48, 49):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (64, 65, 68, 69):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (8, 12, 136, 140):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (3, 35, 131, 163):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (6, 38, 134, 166):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (20, 21, 52, 53):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (144, 145, 176, 177):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (192, 193, 196, 197):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (96, 97, 100, 101):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (40, 44, 168, 172):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (9, 13, 137, 141):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (18, 50):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (80, 81):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (72, 76):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (10, 138):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 66:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 24:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (7, 39, 135):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (148, 149, 180):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (224, 228, 225):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (41, 169, 45):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (22, 54):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (208, 209):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (104, 108):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (11, 139):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (19, 51):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (146, 178):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (84, 85):
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (112, 113):
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]

    elif pattern in (200, 204):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (73, 77):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[BOTTOM] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (42, 170):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (14, 142):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 67:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 70:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 28:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 152:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 194:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 98:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 56:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 25:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (26, 31):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (82, 214):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (88, 248):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (74, 107):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 27:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 86:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 216:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 106:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 30:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 210:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 120:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 75:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 29:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 198:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 184:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 99:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 57:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 71:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 156:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 226:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 60:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 195:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 102:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 153:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 58:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 83:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 92:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 202:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 78:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 154:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 114:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 89:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 90:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (55, 23):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (182, 150):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (213, 212):
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern in (241, 240):
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]

    elif pattern in (236, 232):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (109, 105):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (171, 43):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (143, 15):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 124:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 203:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 62:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 211:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 118:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 217:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 110:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 155:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 188:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 185:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 61:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 157:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 103:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 227:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 230:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 199:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 220:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 158:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 234:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 242:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 59:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 121:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 87:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 79:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 122:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 94:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 218:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 91:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 229:
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 167:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 173:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 181:
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 186:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 115:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 93:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 206:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (205, 201):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (174, 46):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (179, 147):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (117, 116):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 189:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 231:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 126:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 219:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 125:
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 221:
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])

    elif pattern == 207:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 238:
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_even(context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 190:
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[RIGHT], context[CENTER])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 187:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[TOP_LEFT] = mix_even(context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_3_to_1(context[LEFT], context[CENTER])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 243:
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_3_to_1(context[BOTTOM], context[CENTER])
            result[BOTTOM_RIGHT] = mix_even(context[RIGHT], context[BOTTOM])
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]

    elif pattern == 119:
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_3_to_1(context[TOP], context[CENTER])
            result[TOP_RIGHT] = mix_even(context[TOP], context[RIGHT])
            result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern in (237, 233):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern in (175, 47):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern in (183, 151):
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern in (245, 244):
        result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 250:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 123:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 95:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 222:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 252:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 249:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 235:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 111:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 63:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 159:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 215:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 246:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 254:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 253:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP] = mix_3_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 251:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[LEFT] = context[CENTER]
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[RIGHT] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 239:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        result[TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])

    elif pattern == 127:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[TOP] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
            result[BOTTOM] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_7_to_7(context[CENTER], context[BOTTOM], context[LEFT])
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])

    elif pattern == 191:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])

    elif pattern == 223:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
            result[LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_7_to_7(context[CENTER], context[LEFT], context[TOP])
            result[LEFT] = mix_7_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP] = context[CENTER]
            result[TOP_RIGHT] = context[CENTER]
            result[RIGHT] = context[CENTER]
        else:
            result[TOP] = mix_7_to_1(context[CENTER], context[TOP])
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
            result[RIGHT] = mix_7_to_1(context[CENTER], context[RIGHT])
        result[CENTER] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM] = context[CENTER]
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM] = mix_7_to_1(context[CENTER], context[BOTTOM])
            result[BOTTOM_RIGHT] = mix_2_to_7_to_7(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 247:
        result[TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        result[BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    elif pattern == 255:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[TOP_LEFT] = context[CENTER]
        else:
            result[TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[TOP] = context[CENTER]
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[TOP_RIGHT] = context[CENTER]
        else:
            result[TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[LEFT] = context[CENTER]
        result[CENTER] = context[CENTER]
        result[RIGHT] = context[CENTER]
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[BOTTOM_LEFT] = context[CENTER]
        else:
            result[BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[BOTTOM] = context[CENTER]
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[BOTTOM_RIGHT] = context[CENTER]
        else:
            result[BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    return result
