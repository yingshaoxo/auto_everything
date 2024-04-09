#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
Interpolatation functions.
"""
import functools

import auto_everything.additional.hqx.rgb_yuv as rgb_yuv
import auto_everything.additional.hqx.constants as constants

MASK_1_3 = 0x00FF00FF
MASK_2 = 0x0000FF00
MASK_4 = 0xFF000000


@functools.cache
def mix_3_to_1(rgb1_int: int, rgb2_int: int) -> int:
    """
    Analogous to ``Interpolate_2``.

    :param rgb1_int: An RGB integer.
    :param rgb2_int: An RGB integer.
    :return: A resulting RGB integer.
    """
    if rgb1_int == rgb2_int:
        return rgb1_int
    return (
        (((rgb1_int & MASK_2) * 3 + (rgb2_int & MASK_2)) >> 2) & MASK_2
        | (((rgb1_int & MASK_1_3) * 3 + (rgb2_int & MASK_1_3)) >> 2) & MASK_1_3
        | (((rgb1_int & MASK_4) >> 2) * 3 + ((rgb2_int & MASK_4) >> 2)) & MASK_4
    )


@functools.cache
def mix_2_to_1_to_1(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    """
    Analogous to ``Interpolate_3``.

    :param rgb1_int: An RGB integer.
    :param rgb2_int: An RGB integer.
    :param rgb3_int: An RGB integer.
    :return: A resulting RGB integer.
    """
    return (
        (((rgb1_int & MASK_2) * 2 + (rgb2_int & MASK_2) + (rgb3_int & MASK_2)) >> 2) & MASK_2
        | (((rgb1_int & MASK_1_3) * 2 + (rgb2_int & MASK_1_3) + (rgb3_int & MASK_1_3)) >> 2) & MASK_1_3
        | (((rgb1_int & MASK_4) >> 2) * 2 + ((rgb2_int & MASK_4) >> 2) + ((rgb3_int & MASK_4) >> 2)) & MASK_4
    )


@functools.cache
def mix_7_to_1(rgb1_int: int, rgb2_int: int) -> int:
    if rgb1_int == rgb2_int:
        return rgb1_int
    return (
        (((rgb1_int & MASK_2) * 7 + (rgb2_int & MASK_2)) >> 3) & MASK_2
        | (((rgb1_int & MASK_1_3) * 7 + (rgb2_int & MASK_1_3)) >> 3) & MASK_1_3
        | (((rgb1_int & MASK_4) >> 3) * 7 + ((rgb2_int & MASK_4) >> 3)) & MASK_4
    )


@functools.cache
def mix_2_to_7_to_7(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    return (
        (((rgb1_int & MASK_2) * 2 + (rgb2_int & MASK_2) * 7 + (rgb3_int & MASK_2) * 7) >> 4) & MASK_2
        | (((rgb1_int & MASK_1_3) * 2 + (rgb2_int & MASK_1_3) * 7 + (rgb3_int & MASK_1_3) * 7) >> 4) & MASK_1_3
        | (((rgb1_int & MASK_4) >> 4) * 2 + ((rgb2_int & MASK_4) >> 4) * 7 + ((rgb3_int & MASK_4) >> 4) * 7) & MASK_4
    )


@functools.cache
def mix_even(rgb1_int: int, rgb2_int: int) -> int:
    if rgb1_int == rgb2_int:
        return rgb1_int
    return (
        (((rgb1_int & MASK_2) + (rgb2_int & MASK_2)) >> 1 & MASK_2)
        | (((rgb1_int & MASK_1_3) + (rgb2_int & MASK_1_3)) >> 1 & MASK_1_3)
        | (((rgb1_int & MASK_4) >> 1 + (rgb2_int & MASK_4) >> 1) & MASK_4)
    )


@functools.cache
def mix_4_to_2_to_1(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    return (
        (((rgb1_int & MASK_2) * 5 + (rgb2_int & MASK_2) * 2 + (rgb3_int & MASK_2)) >> 3 & MASK_2)
        | (((rgb1_int & MASK_1_3) * 5 + (rgb2_int & MASK_1_3) * 2 + (rgb3_int & MASK_1_3)) >> 3 & MASK_1_3)
        | (((rgb1_int & MASK_4) >> 3 * 5 + (rgb2_int & MASK_4) >> 3 * 2 + (rgb3_int & MASK_4) >> 3) & MASK_4)
    )


@functools.cache
def mix_6_to_1_to_1(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    return (
        (((rgb1_int & MASK_2) * 6 + (rgb2_int & MASK_2) + (rgb3_int & MASK_2)) >> 3 & MASK_2)
        | (((rgb1_int & MASK_1_3) * 6 + (rgb2_int & MASK_1_3) + (rgb3_int & MASK_1_3)) >> 3 & MASK_1_3)
        | (((rgb1_int & MASK_4) >> 3 * 6 + (rgb2_int & MASK_4) >> 3 + (rgb3_int & MASK_4) >> 3) & MASK_4)
    )


@functools.cache
def mix_5_to_3(rgb1_int: int, rgb2_int: int) -> int:
    if rgb1_int == rgb2_int:
        return rgb1_int
    return (
        (((rgb1_int & MASK_2) * 5 + (rgb2_int & MASK_2) * 3) >> 3 & MASK_2)
        | (((rgb1_int & MASK_1_3) * 5 + (rgb2_int & MASK_1_3) * 3) >> 3 & MASK_1_3)
        | (((rgb1_int & MASK_4) >> 3 * 5 + (rgb2_int & MASK_4) >> 3 * 3) & MASK_4)
    )


@functools.cache
def mix_2_to_3_to_3(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    return (
        ((((rgb1_int & MASK_2) * 2 + (rgb2_int & MASK_2) * 3 + (rgb3_int & MASK_2) * 3) >> 3) & MASK_2)
        | ((((rgb1_int & MASK_1_3) * 2 + (rgb2_int & MASK_1_3) * 3 + (rgb3_int & MASK_1_3) * 3) >> 3) & MASK_1_3)
        | ((((rgb1_int & MASK_4) >> 3) * 2 + ((rgb2_int & MASK_4) >> 3) * 3 + ((rgb3_int & MASK_4) >> 3) * 3) & MASK_4)
    )


@functools.cache
def mix_1_4_to_1_to_1(rgb1_int: int, rgb2_int: int, rgb3_int: int) -> int:
    return (
        ((((rgb1_int & MASK_2) * 14 + (rgb2_int & MASK_2) + (rgb3_int & MASK_2)) >> 4) & MASK_2)
        | ((((rgb1_int & MASK_1_3) * 14 + (rgb2_int & MASK_1_3) + (rgb3_int & MASK_1_3)) >> 4) & MASK_1_3)
        | ((((rgb1_int & MASK_4) >> 4) * 14 + ((rgb2_int & MASK_4) >> 4) + ((rgb3_int & MASK_4) >> 4)) & MASK_4)
    )


def generate_pattern(context: list[int], yuv_context: list[int]) -> int:
    """
    Given `context`, a list of surrounding pixels as RGB integers, return a pattern.

    A pattern is a 7 bit integer describing the YUV relationship between the center and a surrounding pixel.
    The "center" bit (4) is skipped and the right pixel takes it place.

    :param context: A list of surrounding pixels as RGB integers, including the center.
    :param yuv_context: Version of `context` but as YUV integers.
    :return: A 7-bit integer of a pattern.
    """
    yuv_px = rgb_yuv.rgb_int_to_yuv_int(context[4])
    pattern = 0
    for bit in range(9):
        if bit != 4 and not rgb_yuv.yuv_equal(yuv_context[bit], yuv_px):
            pattern |= constants.CONTEXT_FLAG[bit]
    return pattern
