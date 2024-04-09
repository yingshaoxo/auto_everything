#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
RGB and YUV functions.
"""

import functools

# Constants defining how far apart two components of YUV colors must be to be considered different
Y_THRESHOLD = 48
U_THRESHOLD = 7
V_THRESHOLD = 6


@functools.cache
def packed_int_to_tuple(packed_int: int) -> tuple[int, int, int]:
    """
    Given `packed_int`, a 24-bit integer containing 3 8-bit values, return a tuple of those three 8-bit integers.

    This is the inverse of :func:`tuple_to_packed_int`.

    :param packed_int: A packed integer.
    :return: A tuple of three 8-bit integers.
    """
    return (packed_int >> 16) & 255, (packed_int >> 8) & 255, packed_int & 255


@functools.cache
def tuple_to_packed_int(unpacked_tuple: tuple[int, int, int]) -> int:
    """
    Given `unpacked_tuple`, a tuple of 3 8-bit integers, return an integer containing these three bytes.

    This is the inverse of :func:`packed_int_to_tuple`.

    :param unpacked_tuple: A tuple of three 8-bit integers.
    :return: A packed integer.
    """
    return unpacked_tuple[0] << 16 | unpacked_tuple[1] << 8 | unpacked_tuple[2]


@functools.cache
def rgb_int_to_yuv_int(rgb: int) -> int:
    """
    Takes an RGB integer and returns a YUV integer.
    Both must be 24-bit color.

    :param rgb: An RGB integer, must be 24-bit.
    :return: A YUV integer.
    """

    red, green, blue = packed_int_to_tuple(rgb)

    y = (red + green + blue) >> 2
    u = 128 + ((red - blue) >> 2)
    v = 128 + ((green * 2 - red - blue) >> 2)

    return tuple_to_packed_int((y, u, v))


@functools.cache
def yuv_equal(yuv1_int: int, yuv2_int: int) -> bool:
    """
    Takes two YUV integers.
    Returns True if they are equal-ish, False otherwise.

    "Equal-ish" is defined arbitrarily as tolerating small differences in the components of the two colors.
    See Y,U,V_THRESHOLD.

    :param yuv1_int: First YUV integer.
    :param yuv2_int: Second YUV integer.
    :return: Boolean if yuv1 and yuv2 are close.
    """
    y1, u1, v1 = packed_int_to_tuple(yuv1_int)
    y2, u2, v2 = packed_int_to_tuple(yuv2_int)
    if abs(y1 - y2) > Y_THRESHOLD:
        return False
    if abs(u1 - u2) > U_THRESHOLD:
        return False
    if abs(v1 - v2) > V_THRESHOLD:
        return False
    return True
