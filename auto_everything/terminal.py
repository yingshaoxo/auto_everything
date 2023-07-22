import signal
from typing import Tuple, List, Callable

import sys
import os
import platform
import tempfile
import hashlib
import time
from datetime import datetime
import shlex
import subprocess
# from multiprocessing import Manager; share_dict = Manager().dict()

import psutil


class Terminal:
    """
    Terminal simulator for execute bash commands
    """

    def __init__(self, debug: bool = False):
        """
        Parameters

        ----------
        username
            Linux system username
        """
        from auto_everything.io import IO

        self.debug: bool = debug

        self.py_version: str = "{major}.{minor}".format(
            major=str(sys.version_info[0]), minor=str(sys.version_info[1])
        )
        self.py_executable: str = sys.executable.replace("\\", "/")
        if os.name == "posix":
            self.system_type: str = "linux"
        elif os.name == "nt":
            self.system_type: str = "win"
        else:
            self.system_type: str = "none"
        self.machine_type: str = platform.machine()

        _2or3 = sys.version_info[0]
        _second_version_number = sys.version_info[1]
        if float(_2or3) <= 2:
            print("We only support Python3")
            exit()
        if (int(_2or3) == 3) and (int(_second_version_number) < 5):
            print("We only support Python >= 3.5")
            exit()

        self.current_dir: str = os.getcwd()
        self.__current_file_path: str = os.path.join(self.current_dir, sys.argv[0])
        self.temp_dir: str = tempfile.gettempdir()

        if os.path.exists(os.path.join(self.current_dir, "nohup.out")):
            os.remove(os.path.join(self.current_dir, "nohup.out"))

        self._io = IO()

    def fix_path(self, path: str, username: str | None = None) -> str:
        # """
        # replace ~ with system username
        # // depressed, please use expanduser_in_path

        # Parameters
        # ----------
        # path : string
        #    A string which contains ~
        # username : string
        #    Linux system username
        # """
        if username is None:
            path = path.replace("~", os.path.expanduser("~"))
        elif username == "root":
            if path[0] == "~":
                path = "~" + path[1:]
        else:
            path = path.replace(
                "~", "/".join(os.path.expanduser("~").split("/")[:-1]) + "/" + username
            )
            print(path)
        return path.replace("\\", "/")

    def expanduser_in_path(self, path: str, username: str | None = None) -> str:
        # """
        # replace ~ with system username

        # Parameters
        # ----------
        # path : string
        #    A string which contains ~
        # username : string
        #    Linux system username
        # """
        return self.fix_path(path, username)

    def exists(self, path: str) -> bool:
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

    def __text_to_sh(self, text: str) -> Tuple[str, str]:
        m = hashlib.sha256()
        m.update(str(datetime.now()).encode("utf-8"))
        m.update(text.encode("utf-8"))
        temp_sh = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".sh")
        # pre_line = f"cd {self.current_dir}\n\n"
        # text = pre_line + text
        self._io.write(temp_sh, text)
        return "bash {path} &".format(path=temp_sh), temp_sh

    def __text_to_py(self, text: str) -> Tuple[str, str]:
        m = hashlib.sha256()
        m.update(str(datetime.now()).encode("utf-8"))
        m.update(text.encode("utf-8"))
        temp_py = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".py")
        self._io.write(temp_py, text)
        return f"{self.py_executable} {temp_py} &", temp_py

    def __remove_temp_sh(self, path: str):
        try:
            os.remove(path)
        except Exception:
            pass

    def run(self, c: str, cwd: str | None = None, wait: bool = True):
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

        if cwd is None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        # if '\n' in c:
        c = self.fix_path(c)
        if self.debug:
            print("\n" + "-" * 20 + "\n")
            print(c)
            print("\n" + "-" * 20 + "\n")
        c, temp_sh = self.__text_to_sh(c)

        try:
            args_list = shlex.split(c)
            p = subprocess.Popen(
                args_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=cwd,
                preexec_fn= None if self.system_type == "win" else os.setsid
            )
        except Exception as e:
            print(e)
            c = self.fix_path(c)
            args_list = shlex.split(c)
            p = subprocess.Popen(
                args_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=cwd,
                preexec_fn= None if self.system_type == "win" else os.setsid
            )

        if wait is True:
            try:
                while p.poll() is None:
                    if p.stdout is None:
                        break
                    line = p.stdout.readline()  # strip(' \n')
                    print(line, end="")
            except KeyboardInterrupt:
                self.__remove_temp_sh(temp_sh)
                self.kill_a_process_by_pid(p.pid)
                raise KeyboardInterrupt
            except Exception as e:
                self.__remove_temp_sh(temp_sh)
                self.kill_a_process_by_pid(p.pid)
                raise e
            self.__remove_temp_sh(temp_sh)
        else:
            return p

    # def advanced_run(self, command: str, current_working_directory: str | None = None, wait: bool = True, share_dict: Any = None):
    #     """
    #     run shell commands without value returning

    #     Parameters
    #     ----------
    #     command: string
    #         shell command
    #     current_working_directory: string
    #         current working directory
    #     wait: bool
    #         True, this command may keep running forever
    #     """

    #     if current_working_directory is None:
    #         current_working_directory = self.current_dir
    #     else:
    #         current_working_directory = self.fix_path(current_working_directory)

    #     # if '\n' in c:
    #     command = self.fix_path(command)
    #     if self.debug:
    #         print("\n" + "-" * 20 + "\n")
    #         print(command)
    #         print("\n" + "-" * 20 + "\n")
    #     command, temp_sh = self.__text_to_sh(command)

    #     try:
    #         args_list = shlex.split(command)
    #         p = subprocess.Popen(
    #             args_list,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT,
    #             universal_newlines=True,
    #             cwd=current_working_directory,
    #             shell=False,
    #             preexec_fn=os.setsid
    #         )
    #     except Exception as e:
    #         print(e)
    #         command = self.fix_path(command)
    #         args_list = shlex.split(command)
    #         p = subprocess.Popen(
    #             args_list,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT,
    #             universal_newlines=True,
    #             cwd=current_working_directory,
    #             shell=False,
    #             preexec_fn=os.setsid
    #         )

    #     if share_dict != None:
    #         share_dict['process_instance'] = p
    #         share_dict['temp_sh_file_path'] = temp_sh

    #     if wait is True:
    #         try:
    #             while p.poll() is None:
    #                 if p.stdout is None:
    #                     break
    #                 line = p.stdout.readline()  # strip(' \n')
    #                 print(line, end="")
    #         except KeyboardInterrupt:
    #             self.kill_a_process_by_pid(p.pid)
    #             self.__remove_temp_sh(temp_sh)
    #             raise KeyboardInterrupt
    #         self.__remove_temp_sh(temp_sh)
    #     else:
    #         return p

    def run_command(self, c: str, timeout: int = 15, cwd: str | None = None) -> str:
        """
        run shell commands with return value

        Parameters
        ----------
        c: string
            shell command
        timeout: int, seconds
            how long this command will take, beyound it, an exception will raise
        cwd: string
            current working directory
        """
        if cwd is None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        # if '\n' in c:
        c = self.fix_path(c)
        if self.debug:
            print("\n" + "-" * 20 + "\n")
            print(c)
            print("\n" + "-" * 20 + "\n")
        c, temp_sh = self.__text_to_sh(c)

        args_list = shlex.split(c)
        try:
            try:
                result = subprocess.run(
                    args_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=cwd,
                    universal_newlines=True,
                    timeout=timeout,
                )
                result = str(result.stdout).strip(" \n")
            except KeyboardInterrupt:
                self.__remove_temp_sh(temp_sh)
                raise KeyboardInterrupt
            self.__remove_temp_sh(temp_sh)
            return result
        except Exception as e:
            self.__remove_temp_sh(temp_sh)
            return str(e)

    def run_python_code(self, code: str, timeout: int = 15, cwd: str | None = None) -> str:
        """
        run python code with return value

        Parameters
        ----------
        code: string
            python_code
        timeout: int, seconds
            how long this command will take, beyound it, an exception will raise
        cwd: string
            current working directory
        """
        c = code 

        if cwd is None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        if self.debug:
            print("\n" + "-" * 20 + "\n")
            print(c)
            print("\n" + "-" * 20 + "\n")
        c, temp_sh = self.__text_to_py(c)

        args_list = shlex.split(c)
        # print(args_list)
        # input("Go on?")
        try:
            try:
                result = subprocess.run(
                    args_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL, #.STDOUT,
                    cwd=cwd,
                    universal_newlines=True,
                    timeout=timeout,
                )
                result = str(result.stdout).strip(" \n")
            except KeyboardInterrupt:
                self.__remove_temp_sh(temp_sh)
                raise KeyboardInterrupt
            self.__remove_temp_sh(temp_sh)
            return result
        except Exception as e:
            self.__remove_temp_sh(temp_sh)
            return str(e)

    def run_program(self, name: str, cwd: str | None = None):
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
        name = self.fix_path(name)

        args_list = shlex.split(name)
        args_list = ["nohup"] + args_list

        if cwd is None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        return subprocess.Popen(args_list, cwd=cwd)  # it return a process

    def __split_args(self, file_path_with_command: str) -> Tuple[str, str]:
        file_path_with_command = file_path_with_command.replace("\\", "/")
        args_list = shlex.split(file_path_with_command)
        file_path = args_list[0]
        if file_path[0] != "~":
            file_path = os.path.abspath(file_path)
        if len(file_path) > 1:
            args = " ".join(args_list[1:])
        else:
            args = ""
        return file_path, args

    def run_py(
        self, file_path_with_command: str, cwd: str | None = None, wait: bool = False
    ):
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
        command = self.py_executable + " {path} {args}".format(path=path, args=args)

        if cwd is None:
            cwd = os.path.dirname(path)

        if wait is False:
            self.run_program(command, cwd=cwd)
        elif wait is True:
            self.run(command, cwd=cwd, wait=True)

    def run_sh(
        self, file_path_with_command: str, cwd: str | None = None, wait: bool = False
    ):
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
        command = "bash {path} {args}".format(path=path, args=args)

        if cwd is None:
            cwd = os.path.dirname(path)

        if wait is False:
            self.run_program(command, cwd=cwd)
        elif wait is True:
            self.run(command, cwd=cwd, wait=True)
    
    def _get_pids(self, name: str) -> List[str]:
        """
        name: what's the name of that program ; string

        get a list of pids, only available in Linux ; [string, ...]
        """
        """
        if self.machine_type == "darwin":
            # it is mac os
            lines = self.run_command(f"pgrep {name}").strip("\n ").splits("\n")
            pids = [i.strip("\n ") for i in lines]
            return pids
        else:
            # it is Linux
            pids = os.listdir("/proc")
            pids = [i for i in pids if i.isdigit()]
            command_lines = [self._io.read(f"/proc/{i}/cmdline") for i in pids]
            target_pids = []
            for pid, command in zip(pids, command_lines):
                if name in command:
                    target_pids.append(pid)
            return target_pids
        """
        pids:list[str] = []
        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                # processName = proc.name()
                process_id = proc.pid
                process_command = " ".join(proc.cmdline())
                if name in process_command:
                    pids.append(str(process_id))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return pids

    def _get_all_running_pids(self) -> List[str]:
        pids:list[str] = []
        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                # processName = proc.name()
                process_id = proc.pid
                pids.append(str(process_id))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return pids

    def is_running(self, name: str) -> bool:
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
    
    def is_running_by_pid(self, pid: int | str) -> bool:
        """
        cheack if a program is running by pid

        Parameters
        ----------
        pid: int
            the process id
        """
        pids = self._get_all_running_pids()
        if str(pid) in pids:
            return True
        else:
            return False
    
    def kill_a_process_by_pid(self, pid: int | str, force: bool = True, wait: bool = False, timeout: int = 30):
        """
        kill a program by its pid(process id)

        Parameters
        ----------
        name: string
            what's the name of that program you want to kill
        force: bool
            kill it directlly or softly.
            some program like ffmpeg, should set force=False
        wait: bool
            true, wait until program totolly quit
        timeout: int
            wait until timeout, use second unit
        """
        if force:
            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
                os.killpg(os.getpgid(int(pid)), signal.SIGKILL)
            except Exception as e:
                print(e)
        else:
            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGINT)  # This is typically initiated by pressing Ctrl+C
            except Exception as e:
                print(e)
        
        if wait is True:
            while self.is_running_by_pid(pid) and timeout > 0:
                time.sleep(1)
                timeout -= 1

            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGQUIT)  # Send the signal to all the process groups
            except Exception as e:
                print(e)

    def kill(
        self, name: str, force: bool = True, wait: bool = False, timeout: int = 30
    ):
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
        timeout: int
            wait until timeout, use second unit
        """
        pids = self._get_pids(name)
        for pid in pids:
            if force:
                self.run_command("kill -s SIGKILL {num}".format(num=pid))
                self.run_command("pkill {name}".format(name=name))
            else:
                self.run_command("kill -s SIGINT {num}".format(num=pid))
                # os.kill(pid, signal.SIGINT) #This is typically initiated by pressing Ctrl+C

        if wait is True:
            while self.is_running(name) and timeout > 0:
                time.sleep(1)
                timeout -= 1

            pids = self._get_pids(name)
            for pid in pids:
                self.run_command("kill -s SIGQUIT {num}".format(num=pid))
                # os.killpg(os.getpgid(int(pid)), signal.SIGQUIT)  # Send the signal to all the process groups


class Terminal_User_Interface:
    """
    A class that you can use to make simple terminal/shell based user interface.
    For example, confirm box, multi-selection, input box
    """
    def clear_screen(self):
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            os.system('clear')
        else:
            # for windows platfrom
            os.system('cls')

    def confirm_box(self, text: str, yes_callback_function: Callable[[], None], no_callback_function: Callable[[], None]):
        """
        terminal_user_interface.confirm_box(
            "Are you sure to delete it?", 
            lambda: print("yes"),
            lambda: print("no"),
        )
        """
        while True:
            self.clear_screen()
            user_response = input(f"{text}(y/n) _").strip()

            if user_response.lower() == "n":
                no_callback_function()
                break
            elif user_response.lower() == "y":
                yes_callback_function()
                break

    def selection_box(self, text: str, selections: list[Tuple[str, Callable[[],None]]]):
        """
        terminal_user_interface = Terminal_User_Interface()
        terminal_user_interface.selection_box(
            "Please do a choice:", 
            [
                ("the_a", lambda: print("You choose a")),
                ("the_b", lambda: print("You choose b"))
            ]
        )
        """
        from string import ascii_letters
        while True:
            self.clear_screen()
            print(text)
            print("\n".join([f"{ascii_letters[index]}.{one[0]}" for index, one in enumerate(selections)]))
            max_index = len(selections)-1
            max_alphabet = ascii_letters[max_index]
            user_response = input(f"What do you choose? (a-{max_alphabet}) _").strip()
            if len(user_response) != 1:
                continue
            else:
                if user_response in ascii_letters[0: max_index + 1]:
                    selections[ascii_letters.find(user_response)][1]()
                    break
    
    def input_box(self, text: str, default_value: str, handle_function: Callable[[str], None]):
        user_response = input(text+" _").strip()
        if (user_response == ""):
            handle_function(default_value)
        else:
            handle_function(user_response)