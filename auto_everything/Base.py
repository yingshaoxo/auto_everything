import os
import sys
import shlex, subprocess


class Base():
    def __init__(self):
        self.py_version = '{major}.{minor}'.format(major=str(sys.version_info[0]), minor=str(sys.version_info[1])) 
        if float(self.py_version) < 3.5:
            print('We only support Python >= 3.5 Versions')
            exit()

        self.current_dir = os.getcwd()
        '''if os.path.exists(os.path.join(self.current_dir, 'nohup.out')):
            os.remove(os.path.join(self.current_dir, 'nohup.out'))'''

    def run_command(self, c):
        args_list = shlex.split(c)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)

    def run_program(self, name):
        args_list = shlex.split(name)
        args_list = ['nohup'] + args_list
        p = subprocess.Popen(args_list)

    def run_py(self, file_path):
        process_name = os.path.join(*file_path.split(os.sep)[-2:])
        if process_name not in self.run_command('ps x'):
            self.run_program('python{version} {path} &'.format(version=self.py_version, path=file_path))

    def is_running(self, name):
        if name in self.run_command('ps x'):
            return True
        else:
            return False


class Batch():
    def __init__(self):
        pass

    def get_current_directory_files(self, directory):
        directory = os.path.abspath(directory)
        files_and_dir = os.listdir(directory)
        files = [os.path.join(directory, f) for f in files_and_dir if os.path.isfile(os.path.join(directory, f))]
        return files


if __name__ == "__main__":
    Base()
    Batch()

