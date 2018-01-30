import os
import sys
import shlex, subprocess


class Base():
    def __init__(self):
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.project_path = os.path.abspath(os.path.join(__file__, "../../"))

        self.py_version = sys.version_info 

    def run_command(self, c):
        args_list = shlex.split(c)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)

    def run_program(self, name):
        args_list = shlex.split(name)
        p = subprocess.Popen(args_list)

    def run_py(self, file_path):
        process_name = os.path.join(*file_path.split(os.sep)[-2:])
        if process_name not in self.run_command('ps x'):
            self.run_program('python{major}.{minor} {path} &'.format(major=str(self.py_version[0]), minor=str(self.py_version[1]), path=file_path))

    def is_running(self, name):
        if name in self.run_command('ps x'):
            return True
        else:
            return False
