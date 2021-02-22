//
// Created by yingshaoxo on 2/16/21.
//

#ifndef AUTO_EVERYTHING_DISK_H
#define AUTO_EVERYTHING_DISK_H

#include "vector"
#include "string"

using namespace std;

vector<string> get_files(string folder);
vector<string> get_folders(string folder);

void write_string_to_file(const string &text, const string &path);
string read_file_as_string(const string &path);



#endif //AUTO_EVERYTHING_DISK_H
