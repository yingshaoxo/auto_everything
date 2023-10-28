import sys
from setuptools import Extension
from setuptools.command.build_ext import build_ext

from setuptools import setup, find_packages
from os.path import dirname, join, abspath

version = "3.30"

# main
file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

# Then let's try to include our cpp extension here


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked."""

    def __str__(self):
        import pybind11

        return pybind11.get_include()


ext_modules = [
    Extension(
        "myx11",
        # Sort input source files to ensure bit-for-bit reproducible builds
        sorted(["auto_everything/x11/myx11.cpp"]),
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
        ],
        language="c++",
    ),
]

# cf http://bugs.python.org/issue26689


def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    import os

    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        fname = f.name
    try:
        compiler.compile([fname], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
        return False
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.
    The newer version is prefered over c++11 (when it is available).
    """
    flags = ["-std=c++17", "-std=c++14", "-std=c++11"]

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError("Unsupported compiler -- at least C++11 support " "is needed!")


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""

    c_opts = {
        "msvc": ["/EHsc"],
        "unix": [],
    }
    l_opts = {
        "msvc": [],
        "unix": ["-lX11", "-lXmu"],
    }

    if sys.platform == "darwin":
        darwin_opts = ["-stdlib=libc++", "-mmacosx-version-min=10.7"]
        c_opts["unix"] += darwin_opts
        l_opts["unix"] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == "unix":
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, "-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")

        for ext in self.extensions:
            ext.define_macros = [
                ("VERSION_INFO", '"{}"'.format(self.distribution.get_version()))
            ]
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


setup(
    name="auto_everything",
    version=version,
    description="do automate things on Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="Linux system automation",
    url="http://github.com/yingshaoxo/auto_everything",
    author="yingshaoxo",
    author_email="yingshaoxo@gmail.com",
    license="MIT",
    setup_requires=["pybind11>=2.5.0"],
    install_requires=[
        "setuptools",
    ],
    extras_require={
        "video": ["numpy", "librosa", "moviepy>=1.0.0,<1.0.1", "pyaudio", "vosk"],
        "gui": ["numpy", "opencv-python", "pyscreenshot", "pytesseract", "pyautogui"],
    },
    include_package_data=False,
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
    zip_safe=False,
)
