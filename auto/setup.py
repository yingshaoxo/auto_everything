from setuptools import setup
from glob import glob

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir, get_include

import sys

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension("auto.terminal",
                      # ["src/terminal.cpp"], #sorted(glob('src/*.cpp'))
                      sorted(
                          glob('src/disk/*.cpp') + \
                          glob('src/terminal/*.cpp')
                      ),
                      include_dirs=[
                          # Path to pybind11 headers
                          # get_include(),
                          'src/disk',
                          'src/terminal',
                      ],
                      # Example: passing in the version to the compiled code
                      define_macros=[('VERSION_INFO', __version__)],
                      ),
    Pybind11Extension("auto.disk",
                      # ["src/disk.cpp"],
                      sorted(glob('src/disk/*.cpp')),
                      include_dirs=[
                          # Path to pybind11 headers
                          # get_include(),
                          'src/disk',
                      ],
                      # Example: passing in the version to the compiled code
                      define_macros=[('VERSION_INFO', __version__)],
                      ),
]

setup(
    name="auto",
    version=__version__,
    author="yingshaoxo",
    author_email="yingshaoxo@gmail.com",
    url="https://github.com/yingshaoxo/auto_everything",
    description="We automate everything with CPP and Python.",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
