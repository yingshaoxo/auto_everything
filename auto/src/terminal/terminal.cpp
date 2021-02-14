#include <pybind11/pybind11.h>
#include <iostream>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int run(int i) {
    std::cout << i <<std::endl;
    return i;
}

namespace py = pybind11;

PYBIND11_MODULE(terminal, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: terminal
        .. autosummary::
           :toctree: _generate
           run
    )pbdoc";

    m.def("run", &run, R"pbdoc(
        Add two numbers
        Some other explanation about the add function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}