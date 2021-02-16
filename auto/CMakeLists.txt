cmake_minimum_required(VERSION 3.17)
project(auto)

set(CMAKE_CXX_STANDARD 17)

include_directories(src/disk)
include_directories(src/terminal)

add_executable(auto
        src/disk/disk.cpp
        src/disk/disk.h
        src/terminal/terminal.cpp)
