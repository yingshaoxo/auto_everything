#!/usr/bin/env python

from auto_everything import base

b = base.Terminal()

print("start...\n\n")

# 1
c = """
mkdir hi
cd hi
ls
"""
b.run(c, wait=True)
