#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


#include "vector"
#include "string"
#include <filesystem>

using namespace std;

//def get_files(self, folder: str, recursive: bool = True, type_limiter: List[str] = None) -> List[str]:
bool exists(string path) {
    return filesystem::exists(path);
}

vector<string> get_files(string folder) {
    vector<string> list_of_files;
    for (const auto &entry : filesystem::directory_iterator(folder)) {
        auto path = entry.path();
        if (!filesystem::is_directory(path)) {
            list_of_files.push_back(path);
        }
    }
    return list_of_files;
}

vector<string> get_folders(string folder) {
    vector<string> list_of_files;
    for (const auto &entry : filesystem::directory_iterator(folder)) {
        auto path = entry.path();
        if (filesystem::is_directory(path)) {
            list_of_files.push_back(path);
        }
    }
    return list_of_files;
}


#include <fstream>
#include <string>
#include <iostream>

void write_string_to_file(const string &text, const string &path) {
    std::ofstream out(path);
    out << text;
    out.close();
}


#include <streambuf>

string read_file_as_string(const string &path) {
    ifstream t(path);
    string str((istreambuf_iterator<char>(t)),
               istreambuf_iterator<char>());
    return str;
}


/*
struct StorageNode {
    string type;
    string name;
    string path;
    vector<StorageNode> children;
};
StorageNode get_storage_tree(string folder) {
    StorageNode node;
    return node;
}
*/


namespace py = pybind11;

PYBIND11_MODULE(disk, m
) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: disk
        .. autosummary::
           :toctree: _generate
            get_storage_tree
    )pbdoc";

    m.def("get_files", &get_files, R"pbdoc(
        get files under a folder
    )pbdoc");

    m.def("get_folders", &get_folders, R"pbdoc(
        get folders under a folder
    )pbdoc");

    m.def("write_string_to_file", &write_string_to_file, R"pbdoc(
        write string to a file
    )pbdoc");

    m.def("read_file_as_string", &read_file_as_string, R"pbdoc(
        read a file and return a string
    )pbdoc");

/*
m.def("get_storage_tree", &get_storage_tree, R"pbdoc(
        get a storage tree under a folder
    )pbdoc");
*/

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
