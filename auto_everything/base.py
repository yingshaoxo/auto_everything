import os
import sys
import shlex
import subprocess
import platform as platform

import re
import getpass
import time

import threading

import json

import psutil


class IO():
    """
    This is for normal IO processing
    """

    def __init__(self):
        self.current_dir = os.getcwd()
        self.__log_path = os.path.join(self.current_dir, 'log')

    def make_sure_sudo_permission(self):
        """
        exit if you don't have sudo permission
        """
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()

    def read(self, file_path):
        """
        read text from txt file

        Parameters
        ----------
        file_path
            txt file path
        """
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
            result = f.read()
        return result

    def write(self, file_path, content):
        """
        write text into txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        """
        with open(file_path, 'w', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def append(self, file_path, content):
        """
        append text at the end of a txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        """
        with open(file_path, 'a', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def __make_sure_txt_exist(self, path):
        if not os.path.exists(path):
            self.write(path, "")

    def read_settings(self, key, defult):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            data = json.loads(text)
            return data[key]
        except Exception as e:
            print(e)
            return defult

    def write_settings(self, key, value):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            try:
                data = json.loads(text)
            except Exception as e:
                print(e)
                data = dict()
            data.update({key: value})
            text = json.dumps(data)
            self.write(settings_path, text)
            return True
        except Exception as e:
            print(e)
            return False

    def log(self, text):
        text = str(text)
        now = time.asctime(time.localtime(time.time()))
        text = '\n'*2 + text + '   ' + '({})'.format(now)
        self.append(self.__log_path, text)


class Terminal():
    """
    Terminal simulator for execute bash commands
    """

    def __init__(self, username=None, debug=False):
        """
        Parameters
        ----------
        username
            Linux system username
        """
        self.__debug = debug

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
        replace ~ with system username
        // depressed, please use expanduser_in_path

        Parameters
        ----------
        path : string 
            A string which contains ~ 
        username : string
            Linux system username
        """
        if username == None:
            path = path.replace('~', os.path.expanduser('~'))
        elif username == 'root':
            if path[0] == '~':
                path = '~' + path[1:]
        else:
            path = path.replace(
                '~', "/home/{username}".format(username=username))
        return path.replace("\\", "/")

    def expanduser_in_path(self, path, username=None):
        """
        replace ~ with system username

        Parameters
        ----------
        path : string 
            A string which contains ~ 
        username : string
            Linux system username
        """
        self.fix_path(path, username)

    def exists(self, path):
        """
        cheack if a file or directory exists
        return true is it exists

        Parameters
        ----------
        path : string 
            the path you want to have a check
        """
        path = self.fix_path(path)
        return os.path.exists(path)

    def __text_to_sh(self, text):
        self._io.write(self.__temp_sh, text)
        return "bash {path} &".format(path=self.__temp_sh)

    def run(self, c, cwd=None, wait=True):
        """
        run shell commands without value returning

        Parameters
        ----------
        c: string
            shell command
        cwd: string
            current working directory
        wait: bool
            True, this command may keep running forever
        """
        if self.__debug:
            print('\n' + '-'*20 + '\n')
            print(c)
            print('\n' + '-'*20 + '\n')

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
        else:
            return p

    def run_command(self, c, timeout=15):
        """
        run shell commands with return value

        Parameters
        ----------
        c: string
            shell command
        timeout: int, seconds
            how long this command will take, beyound it, an exception will raise
        """
        if self.__debug:
            print('\n' + '-'*20 + '\n')
            print(c)
            print('\n' + '-'*20 + '\n')

        if '\n' in c:
            c = self.__text_to_sh(c)

        c = self.fix_path(c)
        args_list = shlex.split(c)
        try:
            result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    cwd=self.current_dir, universal_newlines=True, timeout=timeout)
            result = str(result.stdout).strip(" \n")
            try:
                os.remove(self.__temp_sh)
            except:
                pass
            return result
        except Exception as e:
            return str(e)

    def run_program(self, name, cwd=None):
        """
        run shell commands, especially programs which can be started from terminal. 
        This function will not wait program to be finished.

        Parameters
        ----------
        name: string
            for example: 
                `firefox` or `/opt/v2ray/v2ray`
        cwd: string
            current working directory
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

    def run_py(self, file_path_with_command, cwd=None, wait=False):
        """
        run py_file

        Parameters
        ----------
        file_path_with_command: string
            for example: 
                `hi.py --name yingshaoxo`
        cwd: string
            current working directory
        wait: bool
            if true, it will wait until the python program quit
        """
        path, args = self.__split_args(file_path_with_command)
        path = self.fix_path(path)
        command = self.py_executable + \
            ' {path} {args}'.format(path=path, args=args)

        if cwd == None:
            cwd = os.path.dirname(path)

        if wait == False:
            self.run_program(command, cwd=cwd)
        elif wait == True:
            self.run(command, cwd=cwd, wait=True)

    def run_sh(self, file_path_with_command, cwd=None, wait=False):
        """
        run sh_file

        Parameters
        ----------
        file_path_with_command: string
            for example: 
                `hi.sh --name yingshaoxo`
        cwd: string
            current working directory
        wait: bool
            if true, it will wait until the bash program quit
        """
        path, args = self.__split_args(file_path_with_command)
        path = self.fix_path(path)
        command = 'bash {path} {args}'.format(path=path, args=args)

        if cwd == None:
            cwd = os.path.dirname(path)

        if wait == False:
            self.run_program(command, cwd=cwd)
        elif wait == True:
            self.run(command, cwd=cwd, wait=True)

    def _get_pids(self, name):
        """
        name: what's the name of that program ; string

        get a list of pids, only available in Linux ; [string, ...]
        """
        pids = []
        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                #processName = proc.name()
                process_id = proc.pid
                process_command = ' '.join(proc.cmdline())
                if name in process_command:
                    pids.append(process_id)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return pids
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
        """

    def is_running(self, name):
        """
        cheack if a program is running

        Parameters
        ----------
        name: string
            the program name, for example, `firefox`
        """
        pids = self._get_pids(name)
        if len(pids) > 0:
            return True
        else:
            return False
        """
        if (name in self.run_command('ps x')) or (name in self.run_command('ps -A')):
            return True
        else:
            return False
        """

    def kill(self, name, force=True, wait=False, timeout=30):
        """
        kill a program by its name, depends on `kill pid`

        Parameters
        ----------
        name: string
            what's the name of that program you want to kill
        force: bool
            kill it directlly or softly. 
            some program like ffmpeg, should set force=False
        wait: bool
            true, wait until program totolly quit
        """
        pids = self._get_pids(name)
        for pid in pids:
            if force:
                self.run_command('kill -s SIGKILL {num}'.format(num=pid))
                self.run_command('pkill {name}'.format(name=name))
            else:
                self.run_command('kill -s SIGINT {num}'.format(num=pid))
                #import signal
                # os.kill(pid, signal.SIGINT) #This is typically initiated by pressing Ctrl+C

        if wait == True:
            while (self.is_running(name) and timeout > 0):
                time.sleep(1)
                timeout -= 1
            pids = self._get_pids(name)
            self.run_command('kill -s SIGQUIT {num}'.format(num=pid))

        """
        args_list = shlex.split('sudo pkill {name}'.format(name=name))
        result = subprocess.run(args_list, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)
        """


class OS():
    """
    This is for system stuff
    """

    def __init__(self):
        self._io = IO()
        self._t = Terminal()

    def list_python_packages(self):
        self._io.make_sure_sudo_permission()

        installed_packages = self._t.run_command("sudo pip3 list").lower()
        return installed_packages

    def install_python_package(self, package_name, force=False):
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_python_packages()
        if (force == True) or (package_name not in installed_packages):
            self._t.run(
                "sudo pip3 install {name} --upgrade".format(name=package_name))

    def uninstall_python_package(self, package_name, force=False):
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_python_packages()
        if (force == True) or (package_name in installed_packages):
            self._t.run(
                "sudo pip3 uninstall {name} -y".format(name=package_name))

    def list_packages(self):
        """
        Return a list of apt packages which installed in your computer
        """
        self._io.make_sure_sudo_permission()

        installed_packages = self._t.run_command("sudo apt list").lower()
        return installed_packages

    def install_package(self, package_name, force=False):
        """
        Parameters
        ----------
        package_name: string
            the package you want to install
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_packages()
        if (force == True) or (package_name not in installed_packages):
            self._t.run(
                "sudo apt install {name} -y --upgrade".format(name=package_name))

    def uninstall_package(self, package_name, force=False):
        """
        Parameters
        ----------
        package_name: string
            the package you want to uninstall
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_packages()
        if (force == True) or (package_name in installed_packages):
            self._t.run("sudo apt purge {name} -y".format(name=package_name))


class Python():
    """
    Python model was intended to simplify python development
    """

    def __init__(self):
        self._io = IO()
        self._os = OS()
        self._t = Terminal()

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

                if self.thread == False:
                    while_function()
                else:
                    threading.Thread(target=while_function).start()

            return new_function

    def help(self, object):
        """
        get help information about class or function
        """
        if callable(object):
            from inspect import signature
            arguments = str(signature(object))
            print(object.__name__ + arguments)

            doc = object.__doc__
            if doc:
                print(doc, '\n')
        else:
            from pprint import pprint
            methods = dir(object)
            private_methods = []
            public_methods = []
            for method in methods:
                if "_" == method[:1]:
                    private_methods.append(method)
                else:
                    public_methods.append(method)
            print(private_methods, '\n')
            pprint(public_methods)

    def fire(self, class_name):
        """
        fire is a function that will turn any Python class into a command line interface
        """
        try:
            from fire import Fire
        except Exception as e:
            print(e)
            self.install_package('fire')
        Fire(class_name)

    def make_it_runnable(self, py_file_path=None):
        """
        make python file runnable

        after use this function, you can run the py_file by: ./your_py_script_name.py
        """
        if py_file_path == None or self._t.exists(py_file_path):
            py_file_path = os.path.join(
                self._t.current_dir, sys.argv[0].strip('./'))
        codes = self._io.read(py_file_path)
        expected_first_line = '#!/usr/bin/env {}'.format(self._t.py_executable)
        if codes.split('\n')[0] != expected_first_line:
            codes = expected_first_line + '\n' + codes
            self._io.write(py_file_path, codes)
            self._t.run_command('chmod +x {}'.format(py_file_path))


class Git():
    def __init__(self):
        self._io = IO()
        self._os = OS()
        self._t = Terminal()

    def generate_git_tools(self):
        sh_scripts = ''' 
#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def push(self, comment):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def reset(self):
        t.run("""
git reset --hard HEAD^
""")

py.make_it_runnable()
py.fire(Tools)
'''
        self._io.write("Tools.py", sh_scripts)


class Deploy():
    def __init__(self):
        self._t = Terminal()
        self.file_modification_dict = {}

    def whether_a_file_or_dir_has_changed(self, file_path):
        last_modification_time = os.path.getmtime(file_path)

        def update_dict():
            self.file_modification_dict.update({
                file_path: last_modification_time
            })

        if file_path in self.file_modification_dict:
            if last_modification_time != self.file_modification_dict[file_path]:
                update_dict()
                return True
            else:
                return False
        else:
            update_dict()
            return False


class Super():
    """
    This is for sudo operations in linux
    """

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
        start or create a linux service
        after this, the py_file will keep running as long as the computer is running

        Parameters
        ----------
        name: string
            service name
        py_file_path: string
            a path leads to a python script
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
        stop or cancel a linux service
        after this, the py_file will stop running

        Parameters
        ----------
        name: string
            service name
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
            self._t.run_command('sudo rm {}'.format(service_path))

    def service(self, name, py_file_path):
        """
        start or stop service
        after start, the python script will running forever

        Parameters
        ----------
        name: string
            service name
        py_file_path: string
            a path leads to a python script
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
    pass
