import os
import sys
import shlex
import subprocess
import platform as platform

import re
import getpass
import time

import threading


class IO():
    """
    This is for normal IO process
    """

    def __init__(self):
        self.current_dir = os.getcwd()
        self.__log_path = os.path.join(self.current_dir, 'log')

    def make_sure_sudo_permission(self):
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()

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
        self._t = Terminal()

    def install_package(self, package_name):
        """
        package_name: the package you want to install ; string
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self._t.run_command("sudo pip3 list").lower()
        if package_name not in installed_packages:
            self._t.run("sudo pip3 install {name} --upgrade".format(name=package_name))

    def uninstall_package(self, package_name):
        """
        package_name: the package you want to uninstall ; string
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self._t.run_command("sudo pip3 list").lower()
        if package_name in installed_packages:
            self._t.run(
                "sudo pip3 uninstall {name} -y".format(name=package_name))

    class loop():
        def __init__(self, thread=False):
            """
            new_thread: do you want to open a new thread? True/False
            """
            self.thread = thread

        def __call__(self, func):
            """
            func: a function which you want to run forever
            """
            def new_function(*args, **kwargs):
                def while_function():
                    while 1:
                        try:
                            func(*args, **kwargs)
                            time.sleep(1)
                        except Exception as e:
                            print(e)

                if self.thread == False:
                    while_function()
                else:
                    threading.Thread(target=while_function).start()

            return new_function


class Terminal():
    def __init__(self, username=None):
        self.py_version = '{major}.{minor}'.format(
            major=str(sys.version_info[0]), minor=str(sys.version_info[1]))
        self.py_executable = sys.executable.replace("\\", "/")
        if os.name == "posix":
            self.system_type = "linux"
        elif os.name == "nt":
            self.system_type = "win"
        else:
            self.system_type = "none"
        self.machine_type = platform.machine()
        if float(self.py_version) < 3.5:
            print('We only support Python >= 3.5 Versions')
            exit()

        self.current_dir = os.getcwd()
        self.__temp_sh = os.path.join(self.current_dir, 'temp.sh')
        self.__current_file_path = os.path.join(self.current_dir, sys.argv[0])

        if os.path.exists(os.path.join(self.current_dir, 'nohup.out')):
            os.remove(os.path.join(self.current_dir, 'nohup.out'))

        self._io = IO()

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
        return path.replace("\\", "/")

    def exists(self, path):
        """
        cheack if a file or directory exists
        """
        path = self.fix_path(path)
        return os.path.exists(path)

    def __text_to_sh(self, text):
        self._io.write(self.__temp_sh, text)
        return "bash {path} &".format(path=self.__temp_sh)

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

        try:
            args_list = shlex.split(c)
            p = subprocess.Popen(args_list, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, universal_newlines=True, cwd=cwd)
        except Exception as e:
            print(e)
            c = self.fix_path(c)
            args_list = shlex.split(c)
            p = subprocess.Popen(args_list, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, universal_newlines=True, cwd=cwd)

        if wait == True:
            while p.poll() == None:
                line = p.stdout.readline().strip(' \n')
                print(line)
            try:
                os.remove(self.__temp_sh)
            except:
                pass

        return p

    def run_command(self, c, timeout=15):
        """
        c: shell command
        timeout: seconds. how long this command will take
        """
        c = self.fix_path(c)
        args_list = shlex.split(c)
        try:
            result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    cwd=self.current_dir, universal_newlines=True, timeout=timeout)
            return str(result.stdout).strip(" \n")
        except Exception as e:
            return str(e)

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
        file_path_with_command = file_path_with_command.replace("\\", "/")
        args_list = shlex.split(file_path_with_command)
        file_path = args_list[0]
        if file_path[0] != "~":
            file_path = os.path.abspath(file_path)
        if len(file_path) > 1:
            args = ' '.join(args_list[1:])
        else:
            args = ''
        return file_path, args

    def run_py(self, file_path_with_command, working_dir=None, wait=False):
        if working_dir == None:
            working_dir = self.current_dir

        path, args = self.__split_args(file_path_with_command)
        command = self.py_executable + ' {path} {args} &'.format(
            version=self.py_version, path=path, args=args)
        command = self.fix_path(command)

        if wait == False:
            self.run_program(command, cwd=working_dir)
        elif wait == True:
            self.run(command, cwd=working_dir, wait=True)

    def run_sh(self, file_path_with_command, working_dir=None, wait=False):
        if working_dir == None:
            working_dir = self.current_dir

        path, args = self.__split_args(file_path_with_command)
        command = 'bash {path} {args} &'.format(
            path=path, args=args)
        command = self.fix_path(command)

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

    def kill(self, name, force=True, wait=False):
        """
        name: what's the name of that program you want to kill ; string
        force: kill it directlly or softly. some program like ffmpeg, should set force=False
        wait: wait until program quit. useful for something like ffmpeg

        kill a program by its name, depends on `kill pid`
        """
        pids = self._get_pids(name)
        for pid in pids:
            if force:
                self.run_command('kill -s SIGKILL {num}'.format(num=pid))
            else:
                self.run_command('kill -s SIGQUIT {num}'.format(num=pid))

        if wait == True:
            while (self.is_running(name)):
                time.sleep(1)

        """
        args_list = shlex.split('sudo pkill {name}'.format(name=name))
        result = subprocess.run(args_list, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)
        """

    def _get_pids(self, name):
        """
        name: what's the name of that program ; string

        get a list of pids, only available in Linux ; [string, ...]
        """
        all_running_stuff = self.run_command("ps x")

        lines = all_running_stuff.split("\n")
        lines = [line for line in lines if line.strip("\n ") != ""]

        target_lines = []
        for line in lines:
            if name in line:
                target_lines.append(line)

        pids = []
        for line in target_lines:
            words = line.split(" ")
            words = [word for word in words if word.strip(" ") != ""]
            pid = words[0]
            pids.append(pid)

        return pids

    def install_package(self, package_name):
        """
        package_name: the package you want to install ; string
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.run_command("sudo apt list").lower()
        if package_name not in installed_packages:
            self.run("sudo apt install {name} -y --upgrade".format(name=package_name))

    def uninstall_package(self, package_name):
        """
        package_name: the package you want to uninstall ; string
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.run_command("sudo apt list").lower()
        if package_name in installed_packages:
            self.run("sudo apt purge {name} -y".format(name=package_name))


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
StartLimitBurst=100000
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

    def service(self, name, py_file_path):
        """
        name: service name
        py_file_path: a path leads to a python script

        start or stop service, means you can make a python script running forever
        """
        service_path = "/etc/systemd/system/{name}.service".format(name=name)

        cheack_command = "systemctl status {name} | cat\n".format(name=name)

        if not self._t.exists(service_path):
            self.start_service(name, py_file_path)
        else:
            status = ": inactive" in "\n".join(self._t.run_command(
                cheack_command).split("\n")[:5])
            if status:
                self.start_service(name)
            else:
                self.stop_service(name)


if __name__ == "__main__":
    t = Terminal()
    t._("python")
