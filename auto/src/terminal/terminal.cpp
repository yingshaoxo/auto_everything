#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "disk.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


#include <iostream>
#include <string>
#include <bits/stdc++.h>

using namespace std;

void run(const string &commands) {
    auto c_string = commands.c_str();
    cout << commands << endl;
    system(c_string);
}


#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <array>

string run_command(const string &commands) {
    const char *cmd = commands.c_str();
    array<char, 128> buffer{};
    string result;
    unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

#include<cctype>

vector<string> _get_pids() {
    vector<string> real_pids;
    for (auto &pid : get_folders("/proc")) {
        pid = pid.substr(6, pid.size() - 6);
        if (isdigit(pid[0])) {
            real_pids.push_back(pid);
        }
    }
    return real_pids;
}

#include <map>
#include <sstream>
#include <fstream>

map<string, int> _get_running_processes() {
    /*
     * return a map of <comamnd_line, pid>
     *
     * it reads every pid file like '/proc/2801/cmdline'
     * This read-only file holds the complete command line for the process
     */
    map<string, int> m;
    vector<string> pids = _get_pids();
    for (auto const &pid : pids) {
        auto file_path = "/proc/" + pid + "/cmdline";
        string command_line = read_file_as_string(file_path);
        m.insert(pair<string, int>(command_line, stoi(pid)));
    }
    return m;
}

bool is_running(const string &process_name) {
    auto processes = _get_running_processes();
    for (auto const &item : processes) {
        if (item.first.find(process_name) != string::npos) {
            return true;
        }
    }
    return false;
}

#include <chrono>
#include <thread>
#include <sys/types.h>
#include <signal.h>

void kill_it(const string &process_name, bool force = true) {
    auto processes = _get_running_processes();
    if (force) {
        for (auto const &item : processes) {
            if (item.first.find(process_name) != string::npos) {
                int pid = item.second;
                //run("kill -s SIGKILL " + pid);
                kill(pid, SIGKILL);
            }
        }
        run("pkill " + process_name);
    } else {
        for (auto const &item : processes) {
            if (item.first.find(process_name) != string::npos) {
                int pid = item.second;
                //run("kill -s SIGINT " + pid);
                kill(pid, SIGINT);
            }
        }
    }
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
    )pbdoc");

    m.def("run_command", &run_command, R"pbdoc(
        run some commands and return results
    )pbdoc");

    m.def("_get_pids", &_get_pids, R"pbdoc(
        get pids of running process
    )pbdoc");

    m.def("is_running", &is_running, R"pbdoc(
        check if a process is running
    )pbdoc");

    m.def("kill", &kill_it,
          py::arg("process_name"), py::arg("force") = py::bool_(true),
          R"pbdoc(
        check if a process is running
    )pbdoc");


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
