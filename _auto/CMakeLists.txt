cmake_minimum_required(VERSION 3.17)
project(auto)

#https://gcc.gnu.org/wiki/cxx-modules  for c++20 modules
set(CMAKE_CXX_STANDARD 20)

include_directories(src/disk)
include_directories(src/terminal)

add_executable(auto
        src/disk/disk.cpp
        src/disk/disk.h
        src/terminal/terminal.cpp)
