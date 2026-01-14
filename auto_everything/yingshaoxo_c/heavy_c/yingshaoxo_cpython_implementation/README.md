# ypython
A single header version of python for c.

> 'y' here means 'yingshaoxo'. The full name should be "yingshaoxo's python".

> It should have all python built_in type and functions, for example: https://docs.python.org/3/library/functions.html

## How to use
Just import it like:
```c
#include "./y_python.h"
#include "./y_python_linux.h"
```

> If you need "y_python_windows.h", you need to create your own version of "y_python_linux.h", which means you have to implement all functions in "y_python_linux.h" for windows system.

## Ideas for improving the C code quality
### How to use python to write a c dependencies manager or compiler?

They all require the c coder use relative header importing like `#include "./folder_path/*.h"`

#### Method 1, require every function and variable have unique names, and code is written in .h file, will produce a single ".h file"
1. You have to do a parse on the main.c file, so that you could get the `#include "<.h_file_path>"`
2. Then you do parse again on the .h_file_path to get more ".h header file paths", the final data you get is like a node tree, for each folder level, you have a lot of .h files.
3. put all code from bottom(deepest) to top, into a single .h file, then use gcc to do the compile.

#### Method 2, require every function and variable have unique names, will produce a single ".h file"
1. You have to do a parse on the main.c file, so that you could get the `#include "<.h_file_path>"`, then inside of that .h file folder, you do a search for the same file name .c file, you put the .c file code at the bottom of the .h file.
2. Then you do parse again on the .h_file_path to get more ".h header file paths", the final data you get is like a node tree, for each folder level, you have a lot of .h files.
3. put all code from bottom(deepest in tree) to top, into a single .h file, then use gcc to do the compile.

## How to improve the current c?
1. Make a built_in garbage collector.
2. Make a built_in auto_string, auto_int, auto_float, auto_list, auto_dict, auto_bool, auto_none which could auto doing extention and sharing without you to maully control the memory. Similar to Python built-in data type.

## Todo in this repo
* add a function called "to_string" to all of my types. int, float, bool, none, list, dict class, it needs to have a 'to_string' and 'from_string' functions, so that when I call 'to_string', it will print out a json_compatible string, when I call 'from_string', it will convert json string to memory object

* Use those types to make `json_loads(text)` and `json_dumps(dict)` functions


## Todos

1. Make a auto memory garbage recycle or freeing management system. It has to based on function call stack and variable namespace system. For example, when a function returns, all variables created in that function that uses dynamic memory should free those memory unless parent function uses one of those memory pointer.

2. Figure out how to use a dict to represent a python function, then achieve function call function feature by using c to parse python code in runtime, it definitely related to namespace variable dict management. (What is name space? Global variables -> variables created in a function -> another function's variables created inside of a function. Child function can call parent functions, but parent can't call child functions unless they have a function reference pointer.)

3. Use wchar to replace char* so that our programming language can support utf-8 languages, for example, chinese.

4. Performance improving. Especially things related to list index.
