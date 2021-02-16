#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


#include "vector"
#include "string"
#include <filesystem>

//def get_files(self, folder: str, recursive: bool = True, type_limiter: List[str] = None) -> List[str]:
std::vector<std::string> get_files(std::string folder) {
    std::vector<std::string> list_of_files;
    for (const auto &entry : std::filesystem::directory_iterator(folder)) {
        auto path = entry.path();
        if (!std::filesystem::is_directory(path)) {
            list_of_files.push_back(path);
        }
    }
    return list_of_files;
}

std::vector<std::string> get_folders(std::string folder) {
    std::vector<std::string> list_of_files;
    for (const auto &entry : std::filesystem::directory_iterator(folder)) {
        auto path = entry.path();
        if (std::filesystem::is_directory(path)) {
            list_of_files.push_back(path);
        }
    }
    return list_of_files;
}

/*
struct StorageNode {
    std::string type;
    std::string name;
    std::string path;
    std::vector<StorageNode> children;
};
StorageNode get_storage_tree(std::string folder) {
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
