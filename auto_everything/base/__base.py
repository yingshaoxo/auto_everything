import os
import sys
import shlex
import subprocess

import re
import getpass
import time


class IO():
    """
    This is for normal IO process
    """

    def __init__(self):
        self.current_dir = os.getcwd()
        self.__log_path = os.path.join(self.current_dir, 'log')

    def read(self, file_path):
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
            result = f.read()
        return result

    def write(self, file_path, content):
        with open(file_path, 'w', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def append(self, file_path, content):
        with open(file_path, 'a', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def log(self, text):
        text = str(text)
        now = time.asctime(time.localtime(time.time()))
        text = '\n'*2 + text + '   ' + '({})'.format(now)
        self.append(self.__log_path, text)


class Python():
    def __init__(self):
        self._io = IO()

    def loop(self, func):
        """
        func: a function which you want to run forever
        """
        def new_function(*args, **kwargs):
            while 1:
                try:
                    func(*args, **kwargs)
                    time.sleep(1)
                except Exception as e:
                    print(e)
        return new_function


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

    def fix_path(self, path, username=None):
        """
        path: string, which contains ~
        """
        if username == None:
            path = path.replace('~', os.path.expanduser('~'))
        elif username == 'root':
            path = path.replace('~', "/root")
        else:
            path = path.replace(
                '~', "/home/{username}".format(username=username))
        return path

    def exists(self, path):
        """
        cheack if a file or directory exists
        """
        path = self.fix_path(path)
        return os.path.exists(path)

    def __text_to_sh(self, text):
        with open(self._temp_sh, 'w', encoding="utf-8") as f:
            f.write(text)
        return "bash {path} &".format(path=self._temp_sh)

    def run(self, c, cwd=None, wait=True):
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
                line = p.stdout.readline().strip(' \n')
                print(line)
            try:
                os.remove(self._temp_sh)
            except:
                pass

    def run_command(self, c, timeout=15):
        """
        c: shell command
        timeout: seconds. how long this command will take
        """
        c = self.fix_path(c)
        args_list = shlex.split(c)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                cwd=self.current_dir, universal_newlines=True, timeout=timeout)
        return str(result.stdout)

    def run_program(self, name, cwd=None):
        """
        name: shell command or program path, for example: firefox or /opt/v2ray/v2ray
        cwd: current working directory

        This function will not wait program to finish
        """
        args_list = shlex.split(name)
        args_list = ['nohup'] + args_list

        if cwd == None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

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
            self.run(command, cwd=working_dir, wait=True)

    def is_running(self, name):
        """
        cheack if a program is running, this depends on `ps x`
        """
        if name in self.run_command('ps x'):
            return True
        else:
            return False

    def kill(self, name):
        """
        kill a program by its name, this depends on `pkill program`
        """
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


class Super():
    def __init__(self, username="root"):
        self.__username = username
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()
        if not os.path.exists("/home/{username}".format(username=self.__username)) and self.__username != 'root':
            print("\n You just give me a wroung username!")
            exit()
        self._io = IO()
        self._t = Terminal()

    def __get_service_config(self, py_file_path):
        # working_dir = os.path.abspath(os.path.dirname(py_file_path))
        working_dir = os.path.dirname(py_file_path)
        content = """
[Unit]
Description=auto_everything deamon
After=re-local.service

[Service]
Type=simple
User={username}
WorkingDirectory={working_dir}
Environment=DISPLAY=:0.0
ExecStart=/usr/bin/python3 {py_file_path}
Restart=always
RestartSec=5
StartLimitBurst=3
StartLimitInterval=1s

[Install]
WantedBy=multi-user.target
""".format(username=self.__username, working_dir=working_dir, py_file_path=py_file_path)
        if self.__username == "root":
            content.replace("Environment=DISPLAY=:0.0\n", "")
        return content

    def start_service(self, name, py_file_path=None):
        """
        name: service name
        py_file_path: a path leads to a python script
        """
        service_path = "/etc/systemd/system/{name}.service".format(name=name)

        reload_command = "systemctl daemon-reload\n"
        enable_command = "systemctl enable {name}\n".format(name=name)
        restart_command = "systemctl restart {name}\n".format(name=name)
        stop_command = "systemctl stop {name}\n".format(name=name)
        cheack_command = "systemctl status {name} | cat\n".format(name=name)

        if py_file_path == None:
            if not self._t.exists(service_path):
                print(
                    "You have to give me a python script path, so I can help you run it!")
                exit()
            else:
                self._t.run(restart_command)
        else:
            py_file_path = self._t.fix_path(
                py_file_path, username=self.__username)
            py_file_path = os.path.abspath(py_file_path)
            if not self._t.exists(service_path):
                config = self.__get_service_config(py_file_path)
                self._io.write(service_path, config)
                self._t.run(reload_command)
                self._t.run(enable_command)
                self._t.run(restart_command)
                print(config)
                print('\n' + '-'*11 + '\n')
            else:
                old_config = self._io.read(service_path)
                new_config = self.__get_service_config(py_file_path)
                if old_config != new_config:
                    self._io.write(service_path, new_config)
                    self._t.run(reload_command)
                    self._t.run(enable_command)
                    self._t.run(restart_command)
                    print(new_config)
                    print('\n' + '-'*11 + '\n')
                else:
                    self._t.run(restart_command)
            time.sleep(1)
            print("\n".join(self._t.run_command(
                cheack_command).split("\n")[:6]))

    def stop_service(self, name):
        """
        name: service name
        """
        service_path = "/etc/systemd/system/{name}.service".format(name=name)
        stop_command = "systemctl stop {name}\n".format(name=name)
        disable_command = "systemctl disable {name}\n".format(name=name)
        cheack_command = "systemctl status {name} | cat\n".format(name=name)

        if not self._t.exists(service_path):
            print("You even haven't starting a service yet!")
            exit()
        else:
            self._t.run(stop_command)
            self._t.run(disable_command)
            time.sleep(1)
            print("\n".join(self._t.run_command(
                cheack_command).split("\n")[:6]))
