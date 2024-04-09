#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
CLI (command line interface) front-end to hqx.
It supports ``-o`` (output file) and ``-s`` (scale).
"""
import argparse
import io
import os
import pathlib
import sys

import PIL.Image

import hqx

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="hqx is a family of pixel art scaling algorithms. "
                    "hq2x scales an image by 2x, hq3x by 3x, and hq4x by 4x. "
                    "This is a Python port of hqx, unoptimized. "
                    "It is not intended to be used for videos or scenarios where low latency is required. "
                    "Right now, it only supports RGB, not RGB**A** (no transparency support)."
    )
    parser.add_argument(type=pathlib.Path, help="Path to a readable image file.", dest="infile")

    parser.add_argument(
        "-o",
        "--outfile",
        type=pathlib.Path,
        help="Path to write the scaled image. If a file exists here, it will be overwritten. "
        "If this is omitted, the bytes of the scaled image (in PNG) will be put into stdout.",
    )
    parser.add_argument(
        "-s",
        "--scale",
        default=2,
        choices=(2, 3, 4),
        type=int,
        help="Algorithm scale (2 for hq2x, 3 for hq3x, 4 for hq4x). Default is 2 (hq2x).",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"hqx (python) v{hqx.__version__}",
    )

    args = parser.parse_args()
    outimage = hqx.hqx_scale(PIL.Image.open(args.infile), args.scale)
    if args.outfile:
        # Output to file
        with open(args.outfile, "wb") as openfile:
            outimage.save(openfile)
    else:
        # Output to stdout
        png = io.BytesIO()
        outimage.save(png, format="PNG")

        with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
            stdout.write(png.getvalue())
