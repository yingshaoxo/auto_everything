#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
The hq2x algorithm. Outputs a 2x2 grid.
"""
import auto_everything.additional.hqx.interpolate as interpolate
import auto_everything.additional.hqx.rgb_yuv as rgb_yuv
import auto_everything.additional.hqx.constants as constatants

# Local binding to squeeze some performance (and bytes)
mix_3_to_1 = interpolate.mix_3_to_1
mix_2_to_1_to_1 = interpolate.mix_2_to_1_to_1
mix_4_to_2_to_1 = interpolate.mix_4_to_2_to_1
mix_2_to_3_to_3 = interpolate.mix_2_to_3_to_3
mix_6_to_1_to_1 = interpolate.mix_6_to_1_to_1
mix_1_4_to_1_to_1 = interpolate.mix_1_4_to_1_to_1
yuv_equal = rgb_yuv.yuv_equal

# Context positions
TOP_LEFT = 0
TOP = 1
TOP_RIGHT = 2
LEFT = 3
CENTER = 4
RIGHT = 5
BOTTOM_LEFT = 6
BOTTOM = 7
BOTTOM_RIGHT = 8

# Output grid positions, 2x2
OUT_TOP_LEFT = 0
OUT_TOP_RIGHT = 1
OUT_BOTTOM_LEFT = 2
OUT_BOTTOM_RIGHT = 3


def hq2x_pixel(context: list[int]) -> list[int]:
    """
    Output a 4 integer list (2x2) of the 2x scaled `context`.

    :param context: A 9 integer list of the center and surrounding pixel equalities.
    :return: A 4 integer list (2x2).
    """
    yuv_context = [rgb_yuv.rgb_int_to_yuv_int(rgb) for rgb in context]
    pattern = interpolate.generate_pattern(context, yuv_context)

    result = [0, 0, 0, 0]

    if pattern in (0, 1, 4, 32, 128, 5, 132, 160, 33, 129, 36, 133, 164, 161, 37, 165):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (2, 34, 130, 162):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (16, 17, 48, 49):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (64, 65, 68, 69):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (8, 12, 136, 140):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (3, 35, 131, 163):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (6, 38, 134, 166):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (20, 21, 52, 53):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (144, 145, 176, 177):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern in (192, 193, 196, 197):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern in (96, 97, 100, 101):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (40, 44, 168, 172):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (9, 13, 137, 141):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (18, 50):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (80, 81):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (72, 76):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (10, 138):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 66:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 24:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (7, 39, 135):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (148, 149, 180):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern in (224, 228, 225):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern in (41, 169, 45):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (22, 54):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (208, 209):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (104, 108):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (11, 139):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (19, 51):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (146, 178):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
    elif pattern in (84, 85):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
    elif pattern in (112, 113):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (200, 204):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (73, 77):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (42, 170):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (14, 142):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 67:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 70:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 28:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 152:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 194:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 98:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 56:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 25:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (26, 31):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (82, 214):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (88, 248):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (74, 107):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 27:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 86:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 216:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 106:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 30:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 210:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 120:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 75:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 29:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 198:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 184:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 99:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 57:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 71:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 156:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 226:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 60:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 195:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 102:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 153:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 58:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 83:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 92:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 202:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 78:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 154:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 114:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 89:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 90:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (55, 23):
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern in (182, 150):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
    elif pattern in (213, 212):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
    elif pattern in (241, 240):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (236, 232):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern in (109, 105):
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern in (171, 43):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (143, 15):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 124:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 203:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 62:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 211:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 118:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 217:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 110:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 155:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 188:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 185:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 61:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 157:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 103:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 227:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 230:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 199:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 220:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 158:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 234:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 242:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 59:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 121:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 87:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 79:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 122:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 94:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 218:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 91:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 229:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 167:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 173:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 181:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 186:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 115:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 93:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 206:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern in (205, 201):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_6_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern in (174, 46):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        else:
            result[OUT_TOP_LEFT] = mix_6_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (179, 147):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        else:
            result[OUT_TOP_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern in (117, 116):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
        else:
            result[OUT_BOTTOM_RIGHT] = mix_6_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 189:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 231:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 126:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 219:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 125:
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 221:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[TOP])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
    elif pattern == 207:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
            result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_TOP_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 238:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_3_to_3(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[RIGHT])
    elif pattern == 190:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
            result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
            result[OUT_BOTTOM_RIGHT] = mix_4_to_2_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 187:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        else:
            result[OUT_TOP_LEFT] = mix_2_to_3_to_3(context[CENTER], context[LEFT], context[TOP])
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[LEFT], context[BOTTOM])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 243:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_4_to_2_to_1(context[CENTER], context[BOTTOM], context[LEFT])
            result[OUT_BOTTOM_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 119:
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_4_to_2_to_1(context[CENTER], context[TOP], context[LEFT])
            result[OUT_TOP_RIGHT] = mix_2_to_3_to_3(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern in (237, 233):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern in (175, 47):
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern in (183, 151):
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern in (245, 244):
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 250:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 123:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 95:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 222:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 252:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 249:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 235:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP_RIGHT], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 111:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[RIGHT])
    elif pattern == 63:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_RIGHT], context[BOTTOM])
    elif pattern == 159:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 215:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 246:
        result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[TOP_LEFT], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 254:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP_LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 253:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 251:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[TOP_RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 239:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        result[OUT_TOP_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[RIGHT])
    elif pattern == 127:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_2_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM_RIGHT])
    elif pattern == 191:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM])
        result[OUT_BOTTOM_RIGHT] = mix_3_to_1(context[CENTER], context[BOTTOM])
    elif pattern == 223:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_2_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[BOTTOM_LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_2_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 247:
        result[OUT_TOP_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        result[OUT_BOTTOM_LEFT] = mix_3_to_1(context[CENTER], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])
    elif pattern == 255:
        if not yuv_equal(yuv_context[LEFT], yuv_context[TOP]):
            result[OUT_TOP_LEFT] = context[CENTER]
        else:
            result[OUT_TOP_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[LEFT], context[TOP])
        if not yuv_equal(yuv_context[TOP], yuv_context[RIGHT]):
            result[OUT_TOP_RIGHT] = context[CENTER]
        else:
            result[OUT_TOP_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[TOP], context[RIGHT])
        if not yuv_equal(yuv_context[BOTTOM], yuv_context[LEFT]):
            result[OUT_BOTTOM_LEFT] = context[CENTER]
        else:
            result[OUT_BOTTOM_LEFT] = mix_1_4_to_1_to_1(context[CENTER], context[BOTTOM], context[LEFT])
        if not yuv_equal(yuv_context[RIGHT], yuv_context[BOTTOM]):
            result[OUT_BOTTOM_RIGHT] = context[CENTER]
        else:
            result[OUT_BOTTOM_RIGHT] = mix_1_4_to_1_to_1(context[CENTER], context[RIGHT], context[BOTTOM])

    return result
