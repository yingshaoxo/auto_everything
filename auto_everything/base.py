import os
import time
from typing import Any

from auto_everything.terminal import Terminal
from auto_everything.io import IO
from auto_everything.python import Python #type: ignore


class OS():
    """
    This is for system stuff
    """

    def __init__(self):
        self._io = IO()
        self._t = Terminal()

    def list_python_packages(self):
        self._io.make_sure_sudo_permission()

        installed_packages = self._t.run_command("pip3 list").lower()
        return installed_packages

    def install_python_package(self, package_name: str, force: bool=False):
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_python_packages()
        if (force is True) or (package_name not in installed_packages):
            self._t.run(
                "sudo pip3 install {name} --upgrade".format(name=package_name))

    def uninstall_python_package(self, package_name: str, force: bool=False):
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_python_packages()
        if (force is True) or (package_name in installed_packages):
            self._t.run(
                "sudo pip3 uninstall {name} -y".format(name=package_name))

    def list_packages(self):
        """
        Return a list of apt packages which installed in your computer
        """
        self._io.make_sure_sudo_permission()

        installed_packages = self._t.run_command("apt list").lower()
        return installed_packages

    def install_package(self, package_name: str, force: bool=False):
        """
        Parameters
        ----------
        package_name: string
            the package you want to install
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_packages()
        if (force is True) or (package_name not in installed_packages):
            self._t.run(
                "sudo apt install {name} -y --upgrade".format(name=package_name))

    def uninstall_package(self, package_name: str, force: bool=False):
        """
        Parameters
        ----------
        package_name: string
            the package you want to uninstall
        """
        self._io.make_sure_sudo_permission()

        package_name = package_name.strip(" \n").replace('_', '-').lower()
        installed_packages = self.list_packages()
        if (force is True) or (package_name in installed_packages):
            self._t.run("sudo apt purge {name} -y".format(name=package_name))


class Deploy():
    def __init__(self):
        self._t = Terminal()
        self.file_modification_dict: dict[str, Any] = {}

    def whether_a_file_or_dir_has_changed(self, file_path: str):
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

    def __init__(self, username: str="root"):
        self.__username = username
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()
        if not os.path.exists("/home/{username}".format(username=self.__username)) and self.__username != 'root':
            print("\n You just give me a wroung username!")
            exit()
        self._io = IO()
        self._t = Terminal()

    def __get_service_config(self, py_file_path: str):
        working_dir = os.path.dirname(py_file_path)

        display_number = self._t.run_command("who")
        if "not found" in display_number:
            display = ""
        else:
            display_number = display_number.split("(")[-1].split(")")[0]
            display = "Environment=DISPLAY=" + display_number
        if self.__username == "root":
            display = ""

        content = """
[Unit]
Description=auto_everything deamon
After=re-local.service

[Service]
Type=simple
User={username}
WorkingDirectory={working_dir}
{display}
ExecStart=/usr/bin/python3 {py_file_path}
Restart=always
RestartSec=5
StartLimitBurst=100000
StartLimitInterval=1s

[Install]
WantedBy=multi-user.target
""".format(username=self.__username, working_dir=working_dir, py_file_path=py_file_path, display=display)

        return content

    def start_service(self, name: str, py_file_path: str|None=None):
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
        # stop_command = "systemctl stop {name}\n".format(name=name)
        cheack_command = "systemctl status {name} | cat\n".format(name=name)

        if py_file_path is None:
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
                print('\n' + '-' * 11 + '\n')
            else:
                old_config = self._io.read(service_path)
                new_config = self.__get_service_config(py_file_path)
                if old_config != new_config:
                    self._io.write(service_path, new_config)
                    self._t.run(reload_command)
                    self._t.run(enable_command)
                    self._t.run(restart_command)
                    print(new_config)
                    print('\n' + '-' * 11 + '\n')
                else:
                    self._t.run(restart_command)
            time.sleep(1)
            print("\n".join(self._t.run_command(
                cheack_command).split("\n")[:6]))

    def stop_service(self, name: str):
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

    def service(self, name: str, py_file_path: str):
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
