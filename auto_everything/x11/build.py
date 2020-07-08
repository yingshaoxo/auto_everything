#sudo gcc main.cpp -lstdc++ -lX11 -lXmu -o main
from auto_everything.base import Terminal
t = Terminal()


def compile_python_module(cpp_name, extension_name):
    t.run(
        "g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC "
        "`python3 -m pybind11 --includes` "
        "-I /usr/include/python3.7 -I .  "
        "{0} "
        "-o {1}`python3.7-config --extension-suffix` "
        "-L. -lX11 -lXmu -Wl,-rpath,.".format(cpp_name, extension_name)
    )


def build_cython():
    """ Build the cython extension module """
    print("* Start to build...")

    # Compile and link the cython wrapper library
    compile_python_module("myx11.cpp", "myx11")

    print("* Complete")


build_cython()
