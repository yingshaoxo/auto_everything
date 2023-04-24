import time
import threading
import os
import sys
import re
from pprint import pprint
import copy

from typing import Any, Callable


class Python():
    """
    Python model was intended to simplify python development
    """

    def __init__(self):
        from auto_everything.io import IO
        from auto_everything.base import OS
        from auto_everything.terminal import Terminal
        from auto_everything.disk import Disk
        self._io = IO()
        self._os = OS()
        self._t = Terminal()
        self._disk = Disk()

    def check_if_a_variable_is_a_function(self, function: Any) -> bool:
        return isinstance(function, Callable)

    def list_python_packages(self):
        """
        Return a list of python packages which installed in your computer
        """
        return self._os.list_python_packages()

    def install_package(self, package_name: str):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to install
        """
        self._os.install_python_package(package_name)

    def uninstall_package(self, package_name: str):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to uninstall
        """
        self._os.uninstall_python_package(package_name)

    class loop():
        def __init__(self, interval: int | float=1, thread:bool=False):
            """
            interval: inverval in seconds
            new_thread: do you want to open a new thread? True/False
            """
            self.thread = thread
            self.interval = interval

        def __call__(self, func: Any):
            """
            func: a function which you want to run forever
            """

            def new_function(*args: Any, **kwargs: Any):
                def while_function():
                    while 1:
                        try:
                            func(*args, **kwargs)
                            time.sleep(self.interval)
                        except Exception as e:
                            print(e)

                if self.thread is False:
                    while_function()
                else:
                    threading.Thread(target=while_function).start()

            return new_function

    def help(self, object_: Any):
        """
        get help information about class or function
        """
        from inspect import signature
        if callable(object_):
            arguments = str(signature(object_))
            print(object_.__name__ + arguments)

            doc = object_.__doc__
            if doc:
                print(doc, '\n')
        else:
            methods = dir(object_)
            private_methods: list[str] = []
            public_methods: list[str] = []
            for method in methods:
                if method[:1] == "_":
                    private_methods.append(method)
                else:
                    public_methods.append(method)
            print(private_methods, '\n')
            pprint(public_methods)
            """
            callable_list = inspect.getmembers(object_, predicate=inspect.ismethod) + inspect.getmembers(object_,
                                                                                                         predicate=inspect.isclass)
            callable_list = [(one, one[1].__name__ + str(signature(one[1]))) for one in callable_list]
            not_callable_list = dir(object_)
            for one in callable_list:
                if one[0] in not_callable_list:
                    not_callable_list.remove(one[0])
            not_callable_list = [(one, "") for one in not_callable_list]
            private_methods = []
            public_methods = []
            for one in not_callable_list + callable_list:
                if one[0][:1] == "_":
                    private_methods.append(one[0])
                else:
                    public_methods.append(one)

            print(private_methods, "\n")
            [print(one[0], one[1]) for one in public_methods]
            """

    def fire(self, class_name: Any):
        """
        fire is a function that will turn any Python class into a command line interface
        """
        from fire import Fire #type: ignore
        Fire(class_name)

    def make_it_runnable(self, py_file_path: str|None=None):
        """
        make python file runnable

        after use this function, you can run the py_file by: ./your_py_script_name.py
        """
        if py_file_path is None or self._t.exists(py_file_path):
            py_file_path = os.path.join(
                self._t.current_dir, sys.argv[0].strip('./'))
        if os.path.exists(py_file_path):
            codes = self._io.read(py_file_path)
            expected_first_line = '#!/usr/bin/env {}'.format(self._t.py_executable)
            splits = codes.split('\n')
            found = False
            for line in splits:
                if line == expected_first_line:
                    found = True
                    break
            if found == False:
                codes = expected_first_line + '\n' + codes
                self._io.write(py_file_path, codes)
                self._t.run_command('chmod +x {}'.format(py_file_path))

            if not self._disk.executable(py_file_path):
                self._t.run_command('chmod +x {}'.format(py_file_path))

    def make_it_global_runnable(self, py_file_path: str| None=None, executable_name: str | None=None):
        """
        make python file global runnable

        after use this function, you can run the py_file at anywhere by: your_py_script_name.py
        """
        self.make_it_runnable(py_file_path)

        auto_everything_config_folder = "~/.auto_everything"
        bin_folder = os.path.expanduser(os.path.join(auto_everything_config_folder, "bin"))
        if not self._t.exists(bin_folder):
            self._t.run_command(f"mkdir -p {bin_folder}")

        if py_file_path is None or not self._t.exists(py_file_path):
            py_file_path = os.path.join(
                self._t.current_dir, sys.argv[0].strip('./'))

        is_the_first_running = False 
        runnable_path = None

        if os.path.exists(py_file_path):
            if executable_name == None:
                _, executable_name = os.path.split(py_file_path)
            runnable_path = os.path.join(bin_folder, executable_name)
            if not os.path.exists(runnable_path):
                is_the_first_running = True

            # remove links that the real file has been moved, or, remove links that match this py_file_path but with a different executable name
            files = os.listdir(bin_folder)
            [self._t.run(f"cd {bin_folder}; rm {file}") for file in files if
             not os.path.exists(os.path.join(bin_folder, file))]
            files = self._disk.get_files(bin_folder, recursive=False)
            [self._t.run(f"rm {file}") for file in files if
             os.path.realpath(file) == py_file_path and file != runnable_path]

            self._t.run_command(f"ln -s {py_file_path} {runnable_path}")

            bashrc_path = self._t.fix_path(f"~/.bashrc")
            bashrc_target_line = f'export PATH="$PATH:{bin_folder}"'
            bashrc = self._io.read(bashrc_path)
            if bashrc_target_line not in bashrc.split("\n"):
                bashrc = bashrc + "\n" + bashrc_target_line
                self._t.run_command(f"touch {bashrc_path}")
                self._io.write(bashrc_path, bashrc)
        
        if is_the_first_running and runnable_path:
            print(f"\n\n------------------\n\nYou could run \n\nsource ~/.bashrc\n\nto get started!")
            print(f"\n\n------------------\n\nYou could run \n\n{runnable_path.split('/')[-1]} -- --completion\n\nto get bash completion scripts")

    def print(self, data: Any, limit: int=20):
        """
        print `function help info` or print `dict` with length limit (So you could see the structure easily)
        """
        if callable(data):
            self.help(data)
        else:
            data = copy.deepcopy(data)

            def infinite_loop(the_data: Any) -> Any:
                the_type = type(the_data)
                if the_type == str:
                    return the_data[:limit] + "..."
                elif the_type == dict:
                    for key, value in the_data.items():
                        the_data[key] = infinite_loop(value)
                    return the_data
                elif the_type == list:
                    return [infinite_loop(element) for element in the_data]
                else:
                    return the_data

            data = infinite_loop(data)
            pprint(data)
    
    # def _python_code_preprocess(self, python_code: str):
    #     """
    #     { \n } => {}
    #     ( \n ) => ()
    #     \"\"\" \n \"\"\" => add 4 space before every line
    #     \'\'\' \n \'\'\' => add 4 space before every line
    #     > a remind not to touch the comments followed by a function top defination
    #     """
    #     pass
    
    def generate_documentation_for_a_python_project(self, python_project_folder_path: str, markdown_file_output_folder_path: str, only_generate_those_functions_that_has_docstring: bool=True):
        # code_block_match_rule = r"""(?P<code_block>(?:[ \t]*)(?P<code_head>(?:(?:(?:@(?:.*)\s+)*)*(?:(?:class)|(?:(?:async\s+)*def)))[ \t]*(?:\w+)\s*\((?:.*?)\)(?:[ \t]*->[ \t]*(?:(.*)*))?:)(?P<code_body>(?:\n(?:)(?:[ \t]+[^\n]*)|\n)+))"""
        head_information_regex_rule = r"""(?P<class_or_function_top_defination>(?: *@(?:.*?)\n+)* *(?:\s+(?P<is_class>class)|(?P<is_function>def|async +def)) +(?:(?:\n|.)*?):\n+)(?P<documentation>(?:(?:\s+[\"\']{3}(?:(?:\s|.)*?)[\"|\']{3}\n+)?(?:[ \t]*?\#(?:.*?)\n+)*)*)?(?P<class_or_function_propertys>(?(is_class)((?![ \t]+(?:def|class) )(?:(?:.*?): *(?:.*?) *= *(?:.*?)\n)*)|(?:)))?"""
        for file in self._disk.get_files(folder=python_project_folder_path, recursive=True, type_limiter=[".py"]):
            file_name = self._disk.get_file_name(file)
            if file_name.startswith("_"):
                continue

            raw_content = self._io.read(file)
            result_list = re.findall(pattern=head_information_regex_rule, string=raw_content)
            result_list = [
                {
                    'class_or_function_top_defination': one[0],
                    'is_class': one[1] == 'class',
                    'is_function': one[2] == 'def',
                    'documentation': one[3][0] if len(one[3]) == 1 else one[3],
                    'class_or_function_propertys': one[4]
                } 
                for one in result_list
            ]

            text = ""
            for item in result_list:
                class_or_function_top_defination = item["class_or_function_top_defination"]

                # function_name = class_or_function_top_defination.split(" ")[1]
                # if function_name.startswith("_"):
                #     continue

                documentation = item['documentation']
                # documentation = '\n'.join([one[4:] for one in documentation.split('\n')])
                is_class = item["is_class"]
                class_or_function_propertys = item["class_or_function_propertys"]

                heading_space_counting = 0
                for char in class_or_function_top_defination:
                    if char == " ":
                        heading_space_counting += 1
                    else:
                        break

                documentation = documentation.rstrip()
                if only_generate_those_functions_that_has_docstring == True:
                    if len(documentation.strip()) == 0:
                        continue
                class_or_function_propertys = class_or_function_propertys.rstrip() if is_class else ''

                if len(documentation.strip()) != 0 and len(class_or_function_propertys) != 0:
                    text += f"""
{class_or_function_top_defination.rstrip()}
{documentation.rstrip()}
{class_or_function_propertys}
{' ' * heading_space_counting + ' ' * 4}pass
                    """
                elif len(documentation.strip()) != 0 and len(class_or_function_propertys) == 0:
                    text += f"""
{class_or_function_top_defination.rstrip()}
{documentation.rstrip()}
{' ' * heading_space_counting + ' ' * 4}pass
                    """
                elif len(documentation.strip()) == 0 and len(class_or_function_propertys) != 0:
                    text += f"""
{class_or_function_top_defination.rstrip()}
{class_or_function_propertys}
{' ' * heading_space_counting + ' ' * 4}pass
                    """
                elif len(documentation.strip()) == 0 and len(class_or_function_propertys) == 0:
                    text += f"""
{class_or_function_top_defination.rstrip()}
{' ' * heading_space_counting + ' ' * 4}pass
                    """
            
            markdown_template = f"""
# {file_name}

```python
{text.strip()}
```
            """
            
            output_file_path = self._disk.join_paths(markdown_file_output_folder_path, file_name[:-len(".py")] + ".md") 
            self._io.write(file_path=output_file_path, content=markdown_template)

if __name__ == "__main__":
    py = Python()
    py.print({
        "hi": "dasssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssshgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggglddlahkdhkashgdkagda",
        "ok": {
            "fuck": "dhaslhdhagkdhaksghdashkgsadsagdsalhgsahd",
            "dhashd": "dsahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhagdagdas",
            "dsadf": [{"sdf": "sadddddddddddddddddddddddddddddddddd"}, "asddddddddddddddddddddddddd"]
        }
    }, limit=25)
