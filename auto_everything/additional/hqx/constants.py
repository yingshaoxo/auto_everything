#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: LGPL-2.1-only
"""
Simple constant values for hqx.
Contains context positions and context flags.
"""


# For context input, not output (except hq3x)
TOP_LEFT = 0
TOP = 1
TOP_RIGHT = 2
LEFT = 3
CENTER = 4
RIGHT = 5
BOTTOM_LEFT = 6
BOTTOM = 7
BOTTOM_RIGHT = 8

CONTEXT_FLAG = {0: 1, 1: 2, 2: 4, 3: 8, 5: 16, 6: 32, 7: 64, 8: 128}
"""There are eight flags: the cells in the context, skipping the center (4)."""
