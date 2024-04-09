#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
**hqx** *(high quality scale)* is a family of pixel art scaling algorithms that work
by detecting differences between pixels in the `YUV <https://en.wikipedia.org/wiki/YUV>`_ colorspace.

**hq2x** scales an image by 2x, **hq3x** by 3x, and **hq4x** by 4x.

This is a Python port of hqx, unoptimized.
It is not intended to be used for videos or scenarios where low latency is required.

----

You can either use ```hqx.hqx_scale``, ``hqx.hq2x``, ``hqx.hq3x``, or ``hqx.hq4x``.

>>> import hqx
>>> import PIL.Image
>>> image: PIL.Image.Image = PIL.Image.open(...)
>>> x2:    PIL.Image.Image = hqx.hq2x(image)
>>> x3:    PIL.Image.Image = hqx.hq3x(image)
>>> x4:    PIL.Image.Image = hqx.hq4x(image)
>>> # x2 == hqx.hqx_scale(image, 2))
>>> # x3 == hqx.hqx_scale(image, 3))
>>> # x4 == hqx.hqx_scale(image, 4))

----

hqx (python) is licensed under the
`Lesser GNU Public License v2.1 (LGPL-2.1) <https://spdx.org/licenses/LGPL-2.1-only.html>`_.
"""
import functools
try:
    import PIL.Image
    import PIL.PyAccess
except Exception as e:
    pass

import auto_everything.additional.hqx.rgb_yuv as rgb_yuv
import auto_everything.additional.hqx.algor_hq2x as algor_hq2x
import auto_everything.additional.hqx.algor_hq3x as algor_hq3x
import auto_everything.additional.hqx.algor_hq4x as algor_hq4x

__version__ = "1.0"
__author__ = "WhoAteMyButter"
__description__="the hqx algorithm is under GNU license, but it is just an additional part in auto_everything for image module. so it won't effect the auto_everything is under MIT license."


def yingshaoxo_image_scalling_up_by_using_hqx3(image):
    """
    Scale `image` according to hq3x.
    The returned image will be 3*W, 3*H.
    """
    height, width = image.get_shape()
    source = image.raw_data
    destination = image.create_an_image(height * 3, width * 3)

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return tuple(source[y_coord][x_coord][:-1])

    for x in range(width):
        for y in range(height):
            pixel = algor_hq3x.hq3x_pixel(
                [
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 3
            y_scaled = y * 3

            destination.raw_data[y_scaled][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[0])
            destination.raw_data[y_scaled][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[1])
            destination.raw_data[y_scaled][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[2])
            destination.raw_data[y_scaled + 1][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[3])
            destination.raw_data[y_scaled + 1][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[4])
            destination.raw_data[y_scaled + 1][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[5])
            destination.raw_data[y_scaled + 2][x_scaled ] = rgb_yuv.packed_int_to_tuple(pixel[6])
            destination.raw_data[y_scaled + 2][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[7])
            destination.raw_data[y_scaled + 2][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[8])

    new_height, new_width = destination.get_shape()
    image.resize(new_height, new_width)
    for y in range(new_height):
        for x in range(new_width):
            if image.raw_data[y][x][-1] == 0:
                new_color = [0,0,0,0]
            else:
                new_color = list(destination.raw_data[y][x]) + [255]
            destination.raw_data[y][x] = new_color

    return destination


def yingshaoxo_image_scalling_up_by_using_hqx4(image):
    height, width = image.get_shape()
    source = image.raw_data
    destination = image.create_an_image(height * 4, width * 4)

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return tuple(source[y_coord][x_coord][:-1])

    for x in range(width):
        for y in range(height):
            pixel = algor_hq4x.hq4x_pixel(
                [
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 4
            y_scaled = y * 4

            destination.raw_data[y_scaled][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[0])
            destination.raw_data[y_scaled][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[1])
            destination.raw_data[y_scaled][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[2])
            destination.raw_data[y_scaled][x_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[3])
            destination.raw_data[y_scaled + 1][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[4])
            destination.raw_data[y_scaled + 1][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[5])
            destination.raw_data[y_scaled + 1][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[6])
            destination.raw_data[y_scaled + 1][x_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[7])
            destination.raw_data[y_scaled + 2][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[8])
            destination.raw_data[y_scaled + 2][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[9])
            destination.raw_data[y_scaled + 2][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[10])
            destination.raw_data[y_scaled + 2][x_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[11])
            destination.raw_data[y_scaled + 3][x_scaled] = rgb_yuv.packed_int_to_tuple(pixel[12])
            destination.raw_data[y_scaled + 3][x_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[13])
            destination.raw_data[y_scaled + 3][x_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[14])
            destination.raw_data[y_scaled + 3][x_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[15])

    new_height, new_width = destination.get_shape()
    image.resize(new_height, new_width)
    for y in range(new_height):
        for x in range(new_width):
            if image.raw_data[y][x][-1] == 0:
                new_color = [0,0,0,0]
            else:
                new_color = list(destination.raw_data[y][x]) + [255]
            destination.raw_data[y][x] = new_color

    return destination


def hqx_scale(image, scale: int):
    if scale not in (2, 3, 4):
        raise ValueError("scale must be 2, 3, or 4")
    if scale == 2:
        return hq2x(image)
    if scale == 3:
        return hq3x(image)
    if scale == 4:
        return hq4x(image)
    # This should never happen, just return the image
    return image


def hq2x(image):
    """
    Scale `image` according to hq2x.
    The returned image will be 2*W, 2*H.

    :param image: An instance of ``PIL.Image.Image``.
    :return: A hq2x scaled version of `image`.
    """
    width, height = image.size
    source = image.convert("RGB")
    dest = PIL.Image.new("RGB", (width * 2, height * 2))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = dest.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = algor_hq2x.hq2x_pixel(
                [
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 2
            y_scaled = y * 2

            destgrid[x_scaled, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled + 1, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[3])

    return dest


def hq3x(image):
    """
    Scale `image` according to hq3x.
    The returned image will be 3*W, 3*H.

    :param image: An instance of ``PIL.Image.Image``.
    :return: A hq3x scaled version of `image`.
    """
    width, height = image.size
    source = image.convert("RGB")
    destination = PIL.Image.new("RGB", (width * 3, height * 3))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = destination.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = algor_hq3x.hq3x_pixel(
                [
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 3
            y_scaled = y * 3

            destgrid[x_scaled, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled + 2, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[3])
            destgrid[x_scaled + 1, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[4])
            destgrid[x_scaled + 2, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[5])
            destgrid[x_scaled, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[6])
            destgrid[x_scaled + 1, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[7])
            destgrid[x_scaled + 2, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[8])

    return destination


def hq4x(image):
    width, height = image.size
    source = image.convert("RGB")
    destination = PIL.Image.new("RGB", (width * 4, height * 4))

    # These give direct pixel access via grid[x_coord, y_coord]
    sourcegrid: PIL.PyAccess.PyAccess = source.load()
    destgrid: PIL.PyAccess.PyAccess = destination.load()

    @functools.cache
    def get_px(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        if x_coord < 0:
            x_coord = 0
        elif x_coord >= width:
            x_coord = width - 1

        if y_coord < 0:
            y_coord = 0
        elif y_coord >= height:
            y_coord = height - 1

        return sourcegrid[x_coord, y_coord]

    for x in range(width):
        for y in range(height):
            pixel = algor_hq4x.hq4x_pixel(
                [
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y - 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y)),
                    rgb_yuv.tuple_to_packed_int(get_px(x - 1, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x, y + 1)),
                    rgb_yuv.tuple_to_packed_int(get_px(x + 1, y + 1)),
                ]
            )

            x_scaled = x * 4
            y_scaled = y * 4

            destgrid[x_scaled, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[0])
            destgrid[x_scaled + 1, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[1])
            destgrid[x_scaled + 2, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[2])
            destgrid[x_scaled + 3, y_scaled] = rgb_yuv.packed_int_to_tuple(pixel[3])

            destgrid[x_scaled, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[4])
            destgrid[x_scaled + 1, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[5])
            destgrid[x_scaled + 2, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[6])
            destgrid[x_scaled + 3, y_scaled + 1] = rgb_yuv.packed_int_to_tuple(pixel[7])

            destgrid[x_scaled, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[8])
            destgrid[x_scaled + 1, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[9])
            destgrid[x_scaled + 2, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[10])
            destgrid[x_scaled + 3, y_scaled + 2] = rgb_yuv.packed_int_to_tuple(pixel[11])

            destgrid[x_scaled, y_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[12])
            destgrid[x_scaled + 1, y_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[13])
            destgrid[x_scaled + 2, y_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[14])
            destgrid[x_scaled + 3, y_scaled + 3] = rgb_yuv.packed_int_to_tuple(pixel[15])
    return destination
