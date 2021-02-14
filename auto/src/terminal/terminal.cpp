#include <pybind11/pybind11.h>
#include <iostream>
#include <string>
#include <bits/stdc++.h> 


#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

void run(std::string commands) {
    auto c_string = commands.c_str(); 
    std::system(c_string); 
    //std::cout << "result" <<std::endl;
}


#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <array>
std::string run_commands(std::string commands) {
    const char* cmd = commands.c_str();
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
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
        run some commands
        Some other explanation about the add function.
    )pbdoc");

    m.def("run_commands", &run_commands, R"pbdoc(
        run some commands and return results
        Some other explanation about the add function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
