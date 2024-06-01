import signal
import sys
import os
import platform
import hashlib
from datetime import datetime
import shlex
import subprocess
import shutil
# from multiprocessing import Manager; share_dict = Manager().dict()


def my_print(message="", end="\n", flush=False):
    sys.stdout.write(str(message))
    sys.stdout.write(end)
    if flush == True:
        sys.stdout.flush()


class Terminal:
    """
    Terminal simulator for execute bash commands
    """

    def __init__(self, debug = False):
        """
        Parameters

        ----------
        username
            Linux system username
        """
        from auto_everything.io import IO

        self.debug = debug

        self.py_version = "{major}.{minor}".format(
            major=str(sys.version_info[0]), minor=str(sys.version_info[1])
        )
        self.py_executable = sys.executable.replace("\\", "/")
        if os.name == "posix":
            self.system_type = "linux"
        elif os.name == "nt":
            self.system_type = "win"
        else:
            self.system_type = "none"
        self.machine_type = platform.machine()

        _2or3 = sys.version_info[0]
        _second_version_number = sys.version_info[1]
        if float(_2or3) <= 2:
            my_print("We support better in python3")
            #my_print("We only support Python3")
            #exit()
        if (int(_2or3) == 3) and (int(_second_version_number) < 5):
            my_print("We support better in python >= 3.5")
            #my_print("We only support Python >= 3.5")
            #exit()

        self.current_dir = os.getcwd()
        self.__current_file_path = os.path.join(self.current_dir, sys.argv[0])
        if self.exists("/tmp"):
            self.temp_dir = "/tmp"
        else:
            self.temp_dir = "./"

        if os.path.exists(os.path.join(self.current_dir, "nohup.out")):
            os.remove(os.path.join(self.current_dir, "nohup.out"))

        self._io = IO()

    def fix_path(self, path, username = None, startswith = False):
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
        if startswith == True:
            if not path.startswith("~"):
                return path
            else:
                head_string = ""
                tail_string = path[1:]

                if username is None:
                    head_string = os.path.expanduser("~")
                elif username == "root":
                    head_string = "/root"
                else:
                    head_string = "/".join(os.path.expanduser("~").split("/")[:-1]) + "/" + username

                return head_string + tail_string

        if username is None:
            path = path.replace("~", os.path.expanduser("~"))
        elif username == "root":
            if path[0] == "~":
                path = "~" + path[1:]
        else:
            path = path.replace(
                "~", "/".join(os.path.expanduser("~").split("/")[:-1]) + "/" + username
            )
            my_print(path)
        return path.replace("\\", "/")

    def expanduser_in_path(self, path, username = None):
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

    def software_exists(self, software_name, core_function=True):
        """
        cheack if a software exists
        return true is it exists

        Parameters
        ----------
        software_name : string
            for example, "wget", "curl", "git", "python3", "node"
        """
        if core_function == True:
            if self.exists("/bin/" + software_name) or self.exists("/usr/bin/" + software_name):
                return True
            else:
                return False

        try:
            return shutil.which(software_name) != None
        except Exception as e:
            has_which = False
            if "exists" in self.run_command("""
                if which version >/dev/null; then
                    echo "exists"
                else
                    exit 0
                fi
            """):
                has_which = True

            if has_which:
                if "exists" in self.run_command("""
                    if which {} >/dev/null; then
                        echo "exists"
                    else
                        exit 0
                    fi
                """.format(software_name)):
                    return True
            else:
                if "exists" in self.run_command("""
                    if {} --version >/dev/null; then
                        echo "exists"
                    else
                        exit 0
                    fi
                """.format(software_name)):
                    return True
                else:
                    if self.exists("/bin/" + software_name) or self.exists("/usr/bin/" + software_name):
                        return True

            return False

    def _get_bash_software(self):
        if self.software_exists("bash", core_function=True):
            return "bash"
        elif self.software_exists("sh", core_function=True):
            return "sh"
        return "bash"

    def __text_to_sh(self, text, wait=False):
        m = hashlib.sha256()
        m.update(str(datetime.now()).encode("utf-8"))
        m.update(text.encode("utf-8"))
        temp_sh = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".sh")
        # pre_line = f"cd {self.current_dir}\n\n"
        # text = pre_line + text
        if self.software_exists("sleep", core_function=True):
            text = text + "\n\n" + "sleep 0.01"
        self._io.write(temp_sh, text)
        if wait == False:
            return "{shell} {path} &".format(shell=self._get_bash_software(), path=temp_sh), temp_sh
        else:
            return "{shell} {path}".format(shell=self._get_bash_software(), path=temp_sh), temp_sh

    def __text_to_py(self, text):
        m = hashlib.sha256()
        m.update(str(datetime.now()).encode("utf-8"))
        m.update(text.encode("utf-8"))
        temp_py = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".py")
        self._io.write(temp_py, text)
        return self.py_executable + " " + temp_py + " &", temp_py

    def __remove_temp_sh(self, path):
        try:
            os.remove(path)
        except Exception:
            pass

    def run(self, c, cwd = None, wait = True, use_os_system = False):
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
        use_os_system: bool
            False, if this is ture, it will use os.system() to execute command. This will let this function return None
        """

        if cwd is None:
            cwd = self.current_dir
        else:
            cwd = self.fix_path(cwd)

        # if '\n' in c:
        c = self.fix_path(c)
        if self.debug:
            my_print("\n" + "-" * 20 + "\n")
            my_print(c)
            my_print("\n" + "-" * 20 + "\n")

        if (use_os_system == True):
            c = 'cd "{}"'.format(os.path.abspath(cwd)) + "\n\n" + c
            c, temp_sh = self.__text_to_sh(c, wait=True)
        else:
            c, temp_sh = self.__text_to_sh(c, wait=False)

        if (use_os_system == True):
            try:
                os.system(c)
                self.__remove_temp_sh(temp_sh)
            except Exception as e:
                self.__remove_temp_sh(temp_sh)
                raise e
            return None

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
            my_print(e)
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
                    if p.stdout.readable():
                        char = p.stdout.read(1)
                        my_print(char, end="", flush=True)
                    #line = p.stdout.readline()
                    #my_print(line, end="", flush=True)
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
    #         my_print("\n" + "-" * 20 + "\n")
    #         my_print(command)
    #         my_print("\n" + "-" * 20 + "\n")
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
    #         my_print(e)
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
    #                 my_print(line, end="")
    #         except KeyboardInterrupt:
    #             self.kill_a_process_by_pid(p.pid)
    #             self.__remove_temp_sh(temp_sh)
    #             raise KeyboardInterrupt
    #         self.__remove_temp_sh(temp_sh)
    #     else:
    #         return p

    def _version2_of_run_command(self, c, timeout = 15, cwd = None):
        c, temp_sh = self.__text_to_sh(c)
        args_list = shlex.split(c)
        try:
            result = ""
            start_time = datetime.now()
            p = subprocess.Popen(
                args_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=cwd,
                preexec_fn= None if self.system_type == "win" else os.setsid
            )
            try:
                while p.poll() is None:
                    if p.stdout is None:
                        break
                    if p.stdout.readable():
                        char = p.stdout.read(1)
                        result += char
                        #my_print(char, end="", flush=True)
                    end_time = datetime.now()
                    if (end_time - start_time).seconds > timeout:
                        break
                return result.strip(" \n")
            except KeyboardInterrupt:
                self.__remove_temp_sh(temp_sh)
                self.kill_a_process_by_pid(p.pid)
                raise KeyboardInterrupt
            except Exception as e:
                self.__remove_temp_sh(temp_sh)
                self.kill_a_process_by_pid(p.pid)
                return str(e)
            self.__remove_temp_sh(temp_sh)
            return result
        except Exception as e:
            self.__remove_temp_sh(temp_sh)
            return str(e)

    def run_command(self, c, timeout = 15, cwd = None):
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
        old_c = c
        if self.debug:
            my_print("\n" + "-" * 20 + "\n")
            my_print(c)
            my_print("\n" + "-" * 20 + "\n")
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
            return self._version2_of_run_command(old_c, timeout, cwd)
            return str(e)

    def run_python_code(self, code, timeout = 15, cwd = None):
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
            my_print("\n" + "-" * 20 + "\n")
            my_print(c)
            my_print("\n" + "-" * 20 + "\n")
        c, temp_sh = self.__text_to_py(c)

        args_list = shlex.split(c)
        # my_print(args_list)
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

    def run_program(self, name, cwd = None):
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

    def __split_args(self, file_path_with_command):
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
        self, file_path_with_command, cwd = None, wait = False
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
        self, file_path_with_command, cwd = None, wait = False
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
        command = "{shell} {path} {args}".format(shell=self._get_bash_software(), path=path, args=args)

        if cwd is None:
            cwd = os.path.dirname(path)

        if wait is False:
            self.run_program(command, cwd=cwd)
        elif wait is True:
            self.run(command, cwd=cwd, wait=True)

    def _get_pids(self, name):
        """
        name: what's the name of that program ; string

        get a list of pids, only available in Linux ; [string, ...]
        """
        name = str(name)
        if self.machine_type == "darwin":
            # it is mac os
            lines = self.run_command("pgrep " + name).strip("\n ").split("\n")
            pids = [i.strip("\n ") for i in lines]
            return pids
        else:
            # it is Linux
            pids = os.listdir("/proc")
            pids = [i for i in pids if i.isdigit()]
            command_lines = [self._io.read("/proc/" + i + "/cmdline") for i in pids]
            target_pids = []
            for pid, command in zip(pids, command_lines):
                if name in command:
                    target_pids.append(pid)
            return target_pids

        # pids:list[str] = []
        # # Iterate over all running process
        # for proc in psutil.process_iter():
        #     try:
        #         # Get process name & pid from process object.
        #         # processName = proc.name()
        #         process_id = proc.pid
        #         process_command = " ".join(proc.cmdline())
        #         if name in process_command:
        #             pids.append(str(process_id))
        #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        #         pass
        # return pids

    def _get_all_running_pids(self):
        if self.machine_type == "darwin":
            # it is mac os
            lines = self.run_command('pgrep ""').strip("\n ").split("\n")
            pids = [i.strip("\n ") for i in lines]
            return pids
        else:
            # it is Linux
            pids = os.listdir("/proc")
            pids = [i for i in pids if i.isdigit()]
            return pids

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

    def is_running_by_pid(self, pid):
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

    def kill_a_process_by_pid(self, pid, force = True, wait = False, timeout = 30):
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
        # There might have a bug, by importing this time, it will import './time.py', which is my module than system built_in module
        import time

        if force:
            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
                os.killpg(os.getpgid(int(pid)), signal.SIGKILL)
            except Exception as e:
                my_print(e)
        else:
            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGINT)  # This is typically initiated by pressing Ctrl+C
            except Exception as e:
                my_print(e)

        if wait is True:
            while self.is_running_by_pid(pid) and timeout > 0:
                time.sleep(1)
                timeout -= 1

            try:
                os.killpg(os.getpgid(int(pid)), signal.SIGQUIT)  # Send the signal to all the process groups
            except Exception as e:
                my_print(e)

    def kill(
        self, name, force = True, wait = False, timeout = 30
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
        import time

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

    def confirm_box(self, text, yes_callback_function = None, no_callback_function = None):
        """
        terminal_user_interface.confirm_box(
            "Are you sure to delete it?",
            lambda: print("yes"),
            lambda: print("no"),
        )

        #or

        y_or_n = terminal_user_interface.confirm_box(
            "Are you sure to delete it?",
            None,
            None,
        )
        """
        while True:
            self.clear_screen()
            user_response = input(text + "(y/n) ").strip().lower()

            if user_response.lower() == "n":
                if (no_callback_function != None):
                    no_callback_function()
                return "n"
            elif user_response.lower() == "y":
                if (yes_callback_function != None):
                    yes_callback_function()
                return "y"

    def selection_box(self, text, selections, seperate_page_loading_function = None):
        """
        terminal_user_interface.selection_box(
            "Please do a choice:",
            [
                ("the_a", lambda: print("You choose a")),
                ("the_b", lambda: print("You choose b"))
            ]
        )

        #or

        the_a_or_the_b = terminal_user_interface.selection_box(
            "Please do a choice:",
            [
                ("the_a", None),
                ("the_b", None)
            ]
        )

        ___

        def seperate_page_loading_function(page_size:int, current_page:int):
            all_elements = [
                ("the_a", None),
                ("the_b", None),
                ...
            ]
            index = page_size * current_page
            return all_elements[index: index + page_size]
        """
        import time

        simple_mode = False
        if len(selections) > 0 and type(selections[0]) == str:
            simple_mode = True

        if seperate_page_loading_function == None:
            # single selection, no real time list
            while True:
                self.clear_screen()
                my_print(text)
                if simple_mode == False:
                    my_print("\n".join(["    {}. {}".format(index, one[0]) for index, one in enumerate(selections)]))
                else:
                    my_print("\n".join(["    {}. {}".format(index, one) for index, one in enumerate(selections)]))
                max_index = len(selections)-1
                user_response = input("What do you choose? (0-{}) ".format(str(max_index))).strip()
                try:
                    select_index = int(user_response)
                    if 0 <= select_index <= max_index:
                        if simple_mode == True:
                            return selections[select_index]
                        if selections[select_index][1] != None:
                            selections[select_index][1]() # type: ignore
                        return selections[select_index][0]
                except Exception as e:
                    pass
        else:
            page_size = 10
            current_page = 0
            while True:
                self.clear_screen()
                my_print(text)
                try:
                    selections = seperate_page_loading_function(page_size, current_page)
                    if len(selections) > 0 and type(selections[0]) == str:
                        simple_mode = True

                    if simple_mode == False:
                        my_print("\n".join(["    {}. {}".format(index, one[0]) for index, one in enumerate(selections)]))
                    else:
                        my_print("\n".join(["    {}. {}".format(index, one) for index, one in enumerate(selections)]))
                    my_print()
                    my_print("(n for next_page, p for previous_page, j+number for page_jump)")
                    max_index = len(selections)-1
                    user_response = input("What do you choose? (0-{}) ".format(str(max_index))).strip().lower()

                    if user_response == "n":
                        current_page += 1
                        selections = seperate_page_loading_function(page_size, current_page)
                    elif user_response == "p":
                        current_page -= 1
                        selections = seperate_page_loading_function(page_size, current_page)
                    elif user_response.startswith("j"):
                        temp_user_response = user_response[1:]
                        if all([char.isdigit() for char in temp_user_response]):
                            current_page = int(temp_user_response)
                        selections = seperate_page_loading_function(page_size, current_page)

                    if all([char.isdigit() for char in user_response]):
                        select_index = int(user_response)
                        final_result = None
                        if 0 <= select_index <= max_index:
                            if simple_mode == True:
                                return selections[select_index]

                            if selections[select_index][1] != None:
                                selections[select_index][1]() # type: ignore
                            final_result = selections[select_index][0]

                        if final_result != None:
                            return final_result
                except Exception as e:
                    my_print(e)
                    time.sleep(3)
                    pass

    def input_box(self, text, default_value = "", handle_function = None, with_new_line = False):
        """
        your_name = terminal_user_interface.input_box(
            "Please input your name:",
            "Nobody",
            None
        )
        """
        if with_new_line == False:
            user_response = input(text).strip()
        else:
            def delete_one_char():
                sys.stdout.write("\b")
                sys.stdout.write(" ")
                sys.stdout.write("\b")
                sys.stdout.flush()

            self.clear_screen()
            my_print(text)
            my_print("(press ESC(:ZZ) to end the input)")
            advanced_terminal_user_interface = Advanced_Terminal_User_Interface()
            user_response = ""
            while True:
                char = advanced_terminal_user_interface.get_char_input_in_blocking_way()
                char_id = advanced_terminal_user_interface.get_char_id(char)
                if char_id == 27:
                    # exit
                    my_print("\n", end="", flush=True)
                    break
                elif char_id == 10 or char_id == 13:
                    # newline or enter key
                    user_response += "\n"
                elif char_id == 127:
                    # delete key
                    delete_one_char()
                    user_response = user_response[:-1]
                else:
                    if char.isprintable():
                        user_response += char
                self.clear_screen()
                advanced_terminal_user_interface.sys.stdout.write(user_response)
                my_print("", end="", flush=True)
                #advanced_terminal_user_interface.sys.stdout.flush()

                if user_response.endswith(":ZZ"):
                    user_response = user_response[:-3]
                    my_print("\n", end="", flush=True)
                    break

            user_response = user_response.strip()

        if (user_response == ""):
            user_response = default_value

        if handle_function != None:
            handle_function(user_response)

        return user_response

    def edit_box(self, text, handle_function = None, editor = None):
        """
        editor: str
            vi or vim or gedit
        """
        from auto_everything.disk import Disk
        from auto_everything.io import IO
        disk = Disk()
        io_ = IO()

        terminal = Terminal()
        file_path = disk.get_a_temp_file_path("edit.txt")
        io_.write(file_path, text)

        if editor != None:
            terminal.run(editor + " " + file_path)
        else:
            if terminal.software_exists("vi"):
                terminal.run("vi " + file_path)
            elif terminal.software_exists("vim"):
                terminal.run("vim -u NONE " + file_path)
            elif terminal.software_exists("gedit"):
                terminal.run("gedit " + file_path)
            else:
                raise Exception("You should specify the editor, for example, 'vim'")

        if not disk.exists(file_path):
            new_text = ""
        else:
            new_text = io_.read(file_path)

        disk.remove_a_file(file_path)
        return new_text


class Advanced_Terminal_User_Interface:
    def __init__(self):
        import sys
        import termios
        import tty
        self.sys = sys
        self.termios = termios
        self.tty = tty

    def get_char_input_in_blocking_way(self):
        #https://www.physics.udel.edu/~watson/scen103/ascii.html

        fd = self.sys.stdin.fileno()
        old_settings = self.termios.tcgetattr(fd)

        try:
            self.tty.setraw(self.sys.stdin.fileno())
            char = self.sys.stdin.read(1)
        finally:
            self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)

        return char

    def get_char_id(self, char):
        """
        return int
        """
        char_id = ord(char)
        return char_id

    class NoBlockingTerminal():
        """
        with NoBlockingTerminal() as no_blocking_terminal:
            while True:
                if no_blocking_terminal.is_esc_pressed():
                    break
        """
        def __init__(self):
            import sys
            import termios
            import tty
            import select
            self.sys = sys
            self.termios = termios
            self.tty = tty
            self.select = select

        def __enter__(self):
            self.old_settings = self.termios.tcgetattr(self.sys.stdin)
            self.tty.setcbreak(self.sys.stdin.fileno())
            return self

        def __exit__(self, type, value, traceback):
            self.termios.tcsetattr(self.sys.stdin, self.termios.TCSADRAIN, self.old_settings)

        def get_char(self):
            if self.select.select([self.sys.stdin], [], [], 0) == ([self.sys.stdin], [], []):
                return self.sys.stdin.read(1)
            return None

        def is_esc_pressed(self):
            if self.get_char() == '\x1b':  # x1b is ESC
                return True
            else:
                return False


#Instead of using type in function, you can directly put the type after variable name, so that python2 could run it, for example:
#
#def hi(greeting_string):
#    result_string = "yingshaoxo: " + greeting_string
#    return result_string
#
#Normally, all we need is function_name_complete, variable_name_complete, class_function_name_complete, it can be done with regex expression, so no need for using type hint.


if __name__ ==  "__main__":
    terminal = Terminal()
    my_print(terminal.software_exists("vi"))

    terminal_user_interface = Terminal_User_Interface()
    #result = terminal_user_interface.input_box("Please do the input: ", with_new_line=True)
    result = terminal_user_interface.edit_box("You can do edit of this text\n\nIt is fun.", editor="vim")
    my_print(result)
