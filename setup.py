from setuptools import Extension
from setuptools.command.build_ext import build_ext

from setuptools import setup, find_packages
from os.path import dirname, join, abspath

version = "3.12"

# main
file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

# Let's first try to install the normal version
setup(
    name="auto_everything",
    version=version,
    description="do automate things on Linux",
    python_requires=">=3.10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    keywords="Linux system automation",
    url="http://github.com/yingshaoxo/auto_everything",
    author="yingshaoxo",
    author_email="yingshaoxo@gmail.com",
    license="GPLv3",
    install_requires=[
        "setuptools",
        "fire",
        "psutil",
    ],
    extras_require={
        "database": ["pymongo"],
        "video": ["numpy", "librosa", "moviepy", "pyaudio", "vosk"],
        "gui": ["numpy", "opencv-python", "pyscreenshot", "pytesseract", "pyautogui"],
        "fakecamera": ["pyfakewebcam", "opencv-python"],
        "image": ["pillow"],
        "all": ["o365"],
    },
    include_package_data=False,
    packages=["auto_everything"],
)
