import os
import sys
import shlex
import subprocess

import re
import getpass
import time


class Terminal():
    def __init__(self):
        self.py_version = '{major}.{minor}'.format(
            major=str(sys.version_info[0]), minor=str(sys.version_info[1]))
        if float(self.py_version) < 3.5:
            print('We only support Python >= 3.5 Versions')
            exit()

        self.current_dir = os.getcwd()
        self._temp_sh = os.path.join(self.current_dir, 'temp.sh')
        self._current_file_path = os.path.join(self.current_dir, sys.argv[0])

        # if os.path.exists(os.path.join(self.current_dir, 'nohup.out')):
        #     os.remove(os.path.join(self.current_dir, 'nohup.out'))

    def fix_path(self, path):
        return path.replace('~', os.path.expanduser('~'))

    def exists(self, path):
        path = self.fix_path(path)
        return os.path.exists(path)

    def __text_to_sh(self, text):
        with open(self._temp_sh, 'w', encoding="utf-8") as f:
            f.write(text)
        return "bash {path} &".format(path=self._temp_sh)

    def run(self, c, cwd=None, wait=False):
        """
        c: shell command
        cwd: current working directory
        wait: True may running forever
        """
        if cwd == None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        if '\n' in c:
            c = self.__text_to_sh(c)

        args_list = shlex.split(c)
        p = subprocess.Popen(args_list, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, universal_newlines=True, cwd=cwd)

        if wait == True:
            print('')
            while p.poll() == None:
                line = p.stdout.readline().strip(' ')
                print(line)
            try:
                os.remove(self._temp_sh)
            except:
                pass

    def run_command(self, c, timeout=15):
        c = self.fix_path(c)
        args_list = shlex.split(c)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                cwd=self.current_dir, universal_newlines=True, timeout=timeout)
        return str(result.stdout)

    def run_program(self, name, cwd=None):
        args_list = shlex.split(name)
        args_list = ['nohup'] + args_list

        if working_dir == None:
            working_dir = self.current_dir

        p = subprocess.Popen(args_list, cwd=cwd)

    def __split_args(self, file_path_with_command):
        args_list = shlex.split(file_path_with_command)
        file_path = os.path.abspath(args_list[0])
        if len(file_path) > 1:
            args = ' '.join(args_list[1:])
        else:
            args = ''
        return file_path, args

    def run_py(self, file_path_with_command, working_dir=None, wait=False):
        if working_dir == None:
            working_dir = self.current_dir

        path, args = self.__split_args(file_path_with_command)
        path = self.fix_path(path)
        command = '/usr/bin/python{version} {path} {args} &'.format(
            version=self.py_version, path=path, args=args)

        if wait == False:
            self.run_program(command, cwd=working_dir)
        elif wait == True:
            self.run(command, cwd=working_dir, wait=True)

    def run_sh(self, file_path_with_command, working_dir=None, wait=False):
        if working_dir == None:
            working_dir = self.current_dir

        path, args = self.__split_args(file_path_with_command)
        path = self.fix_path(path)
        command = 'bash {path} {args} &'.format(
            path=self.fix_path(path), args=args)

        if wait == False:
            self.run_program(command, cwd=working_dir)
        elif wait == True:
            self.run(command, working_dir=working_dir, wait=True)

    def is_running(self, name):
        if name in self.run_command('ps x'):
            return True
        else:
            return False

    def kill(self, name):
        args_list = shlex.split('sudo pkill {name}'.format(name=name))
        result = subprocess.run(args_list, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)


class Batch():
    def __init__(self):
        pass

    def get_current_directory_files(self, directory):
        directory = os.path.abspath(directory)
        files_and_dir = os.listdir(directory)
        files = [os.path.join(directory, f) for f in files_and_dir if os.path.isfile(
            os.path.join(directory, f))]
        return files
