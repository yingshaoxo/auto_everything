#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "disk.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include <iostream>
#include <string>
#include <bits/stdc++.h>

void run(const std::string &commands) {
    auto c_string = commands.c_str();
    std::system(c_string);
    //std::cout << "result" <<std::endl;
}

#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <array>

std::string run_command(const std::string &commands) {
    const char *cmd = commands.c_str();
    std::array<char, 128> buffer{};
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

// /proc/2801/cmdline
// This read-only file holds the complete command line for the process
#include<cctype>

std::vector<std::string> get_pids() {
    std::vector<std::string> real_pids;
    for (auto &pid : get_folders("/proc")) {
        pid = pid.substr(6, pid.size() - 6);
        if (isdigit(pid[0])) {
            real_pids.push_back(pid);
        }
    }
    return real_pids;
}


namespace py = pybind11;

PYBIND11_MODULE(terminal, m
) {
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

    m.def("run_command", &run_command, R"pbdoc(
        run some commands and return results
        Some other explanation about the add function.
    )pbdoc");

    m.def("get_pids", &get_pids, R"pbdoc(
        get pids of running process
        Some other explanation about the add function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
