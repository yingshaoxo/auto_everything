import time
import threading
import os
import sys


class Python():
    """
    Python model was intended to simplify python development
    """

    def __init__(self):
        from auto_everything.io import IO
        from auto_everything.base import OS
        from auto_everything.terminal import Terminal
        from auto_everything.disk import  Disk
        self._io = IO()
        self._os = OS()
        self._t = Terminal()
        self._disk = Disk()

    def list_python_packages(self):
        """
        Return a list of python packages which installed in your computer
        """
        return self._os.list_python_packages()

    def install_package(self, package_name):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to install
        """
        self._os.install_python_package(package_name)

    def uninstall_package(self, package_name):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to uninstall
        """
        self._os.uninstall_python_package(package_name)

    class loop():
        def __init__(self, interval=1, thread=False):
            """
            new_thread: do you want to open a new thread? True/False
            """
            self.thread = thread
            self.interval = interval

        def __call__(self, func):
            """
            func: a function which you want to run forever
            """

            def new_function(*args, **kwargs):
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

    def help(self, object_):
        """
        get help information about class or function
        """
        if callable(object_):
            from inspect import signature
            arguments = str(signature(object_))
            print(object_.__name__ + arguments)

            doc = object_.__doc__
            if doc:
                print(doc, '\n')
        else:
            from pprint import pprint
            methods = dir(object_)
            private_methods = []
            public_methods = []
            for method in methods:
                if method[:1] == "_":
                    private_methods.append(method)
                else:
                    public_methods.append(method)
            print(private_methods, '\n')
            pprint(public_methods)

    def fire(self, class_name):
        """
        fire is a function that will turn any Python class into a command line interface
        """
        from fire import Fire
        Fire(class_name)

    def make_it_runnable(self, py_file_path=None):
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
            if codes.split('\n')[0] != expected_first_line:
                codes = expected_first_line + '\n' + codes
                self._io.write(py_file_path, codes)
                self._t.run_command('chmod +x {}'.format(py_file_path))
            if not self._disk.executable(py_file_path):
                self._t.run_command('chmod +x {}'.format(py_file_path))

    def make_it_global_runnable(self, py_file_path=None, executable_name=None):
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

        if os.path.exists(py_file_path):
            if executable_name == None:
                _, executable_name = os.path.split(py_file_path)
            runnable_path = os.path.join(bin_folder, executable_name)

            # remove links that the real file has been moved, or, remove links that match this py_file_path but with a different executable name
            files = os.listdir(bin_folder)
            [self._t.run(f"cd {bin_folder}; rm {file}") for file in files if not os.path.exists(os.path.join(bin_folder, file))]
            files = self._disk.get_files(bin_folder, recursive=False)
            [self._t.run(f"rm {file}") for file in files if os.path.realpath(file) == py_file_path and file != runnable_path]

            self._t.run_command(f"ln -s {py_file_path} {runnable_path}")

            bashrc_path = self._t.fix_path(f"~/.bashrc")
            bashrc_target_line = f'export PATH="$PATH:{bin_folder}"'
            bashrc = self._io.read(bashrc_path)
            if bashrc_target_line not in bashrc.split("\n"):
                bashrc = bashrc + "\n" + bashrc_target_line
                self._io.write(bashrc_path, bashrc)
