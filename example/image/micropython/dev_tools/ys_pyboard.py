# The MIT License (MIT)
# Copyright (c) 2014-2021 Damien P. George
# Copyright (c) 2017 Paul Sokolovsky
# Copyright (c) 2024 yingshaoxo

"""
pyboard interface

This module provides the Pyboard class, used to communicate with and
control the pyboard over a serial USB connection.

Example usage:

    import pyboard
    pyb = pyboard.Pyboard('/dev/ttyACM0')
    pyb.enter_raw_repl()
    pyb.exec('pyb.LED(1).on()')
    print(pyb.exec('print(1+1)'))
    pyb.exit_raw_repl()

To run a script from the local machine on the board and print out the results:

    import pyboard
    pyboard.execfile('test.py', device='/dev/ttyACM0')

This script can also be run directly.  To execute a local script, use:

    python pyboard.py test.py

"""

import time
import os


class Pyboard:
    def __init__(self, serial_device, baudrate=115200):
        # the baudrate is 115200 for micropython project
        try:
            import serial
            self.serial = serial.Serial(serial_device, baudrate=baudrate)
            self._in_waiting = None #Return the number of bytes in the receive buffer.
            if "in_waiting" in dir(self.serial):
                def inWaiting():
                    return self.serial.in_waiting
                self._in_waiting = inWaiting
            else:
                self._in_waiting = self.serial.inWaiting
        except Exception as e:
            #print(e)
            from auto_everything.network_ import Serial
            self.serial = Serial(serial_device, baudrate=baudrate)
            self._in_waiting = self.serial.inWaiting

    def close(self):
        self.serial.close()

    def read_until(self, min_num_bytes, ending, timeout=10):
        data = self.serial.read(min_num_bytes)
        timeout_count = 0
        while True:
            if self._in_waiting() > 0:
                data = data + self.serial.read(self._in_waiting())
                time.sleep(0.01)
                timeout_count = 0
            elif data.endswith(ending):
                break
            else:
                timeout_count += 1
                if timeout_count >= 10 * timeout:
                    break
                time.sleep(0.1)
        return data

    def enter_raw_repl(self):
        self.serial.write(b'\r\x03') # ctrl-C: interrupt any running program
        self.serial.write(b'\r\x01') # ctrl-A: enter raw REPL
        self.serial.write(b'\x04') # ctrl-D: soft reset
        data = self.read_until(1, b'to exit\r\n>')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            print(data)
            raise Exception('could not enter raw repl')

    def exit_raw_repl(self):
        self.serial.write(b'\r\x02') # ctrl-B: enter friendly REPL

    def eval(self, expression):
        ret = self.exec('print({})'.format(expression))
        ret = ret.strip()
        return ret

    def exec(self, command):
        command_bytes = bytes(command, encoding='ascii')
        for i in range(0, len(command_bytes), 32):
            self.serial.write(command_bytes[i:min(i+32, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')
        data = self.serial.read(2)
        if data != b'OK':
            print(data)
            raise Exception('could not exec command')
        data = self.read_until(2, b'\x04>')
        if not data.endswith(b'\x04>'):
            print(data)
            raise Exception('timeout waiting for EOF reception')
        if data.startswith(b'Traceback') or data.startswith(b'  File '):
            print(data)
            raise Exception('command failed')
        return data[:-2]

    def execfile(self, filename):
        with open(filename) as f:
            pyfile = f.read()
        return self.exec(pyfile)

    def get_time(self):
        t = str(self.eval('pyb.RTC().datetime()'), encoding='ascii')[1:-1].split(', ')
        return int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6])

    def run(self, code):
        result = self.exec(code)
        if result.endswith(b"\r\n\x04"):
            result = result[:-3]
        return result.decode("utf-8", errors="ignore")

    def list_files_and_folders(self, folder_path="./"):
        script_content = """
import os
print(os.listdir("{folder_path}"))
        """.strip().format(
            folder_path=folder_path,
        )
        data_string = self.run(script_content)
        return eval(data_string)

    def fs_writefile(self, dest, data, chunk_size=256):
        self.exec("f=open('%s','wb')\nw=f.write" % dest)
        while data:
            chunk = data[:chunk_size]
            self.exec("w(" + repr(chunk) + ")")
            data = data[len(chunk) :]
        self.exec("f.close()")

    def upload_file(self, source_file_path, target_file_path):
        if not os.path.exists(source_file_path):
            raise Exception("File not exists: {}".format(source_file_path))
        if not os.path.isfile(source_file_path):
            return

        #if os.path.islink(source_file_path):
        #    return

        a_file = open(source_file_path, "rb")
        bytes_data = a_file.read()
        a_file.close()

        script_content = """
import os
try:
    os.stat("{folder_path}")
except Exception as e:
    folder_path_splits = "{folder_path}".split("/")
    parent_folder = ""
    for part in folder_path_splits:
        try:
            parent_folder += "/" + part
            os.mkdir(parent_folder)
        except Exception as e:
            pass
        """.strip().format(
            folder_path=os.path.dirname(target_file_path)
        )
        self.exec(script_content)
        self.fs_writefile(target_file_path, bytes_data)
        return

        script_content = """
the_bytes_list = [{int_byte_list_string}]

a_file = open("{file_path}", "wb")
a_file.write(bytes(the_bytes_list))
a_file.close()
        """.strip().format(
            int_byte_list_string=",".join([str(one) for one in bytes_data]),
            file_path=target_file_path,
            folder_path=os.path.dirname(target_file_path)
        )
        self.exec(script_content)

    def delete_file_or_folder(self, target_file_path):
        script_content = """
import os

def exists(path):
    try:
        os.stat(path)
        return True
    except Exception as e:
        return False

def file_exists(path):
    try:
        f = open(path, "r")
        f.close()
        return True
    except Exception as e:
        return False

def dir_exists(path):
    try:
        if os.stat(path)[0] & 0x4000:
            return True
        else:
            return False
    except Exception as e:
        return False

def recursive_delete(target_file_path):
    if not exists(target_file_path):
        return

    if file_exists(target_file_path):
        os.remove(target_file_path)
    elif dir_exists(target_file_path):
        sub_list = os.listdir(target_file_path)
        for a_path in sub_list:
            recursive_delete(target_file_path + "/" + a_path)
        os.rmdir(target_file_path)

the_target_file_path = "{target_file_path}"
recursive_delete(the_target_file_path)
        """.strip().format(
            target_file_path=target_file_path.rstrip("/"),
        )
        self.exec(script_content)

    def sync_folder(self, source_folder, target_folder):
        from auto_everything.disk import Disk
        disk = Disk()

        if len(target_folder) != 1:
            target_folder = target_folder.rstrip("/")
        if not target_folder.startswith("/"):
            raise Exception("The target_folder should starts with '/', it is a absolute path")
        if not source_folder.startswith("./"):
            raise Exception("The source_folder should starts with './', it is a relative path")

        if not os.path.exists(source_folder):
            raise Exception("Folder not exists: {}".format(source_folder))
        if os.path.isfile(source_folder):
            return

        try:
            self.delete_file_or_folder(target_folder)
        except Exception as e:
            print(e)

        for path in disk.get_files(source_folder, use_gitignore_file=True):
            if path.startswith("./"):
                print("In upload:", path)
                self.upload_file(path, os.path.join(target_folder, path))


def execfile(filename, device='/dev/ttyACM0'):
    pyb = Pyboard(device)
    pyb.enter_raw_repl()
    output = pyb.execfile(filename)
    print(str(output, encoding='ascii'), end='')
    pyb.exit_raw_repl()
    pyb.close()

def run_test_for_pyboard():
    # pi pico is not supported
    device = '/dev/ttyACM0'
    pyb = Pyboard(device)
    pyb.enter_raw_repl()
    print('opened device {}'.format(device))

    print('seconds since boot:', pyb.get_time())

    pyb.exec('def apply(l, f):\r\n for item in l:\r\n  f(item)\r\n')

    pyb.exec('leds=[pyb.LED(l) for l in range(1, 5)]')
    pyb.exec('apply(leds, lambda l:l.off())')

    ## USR switch test
    pyb.exec('switch = pyb.Switch()')

    for i in range(2):
        print("press USR button")
        pyb.exec('while switch(): pyb.delay(10)')
        pyb.exec('while not switch(): pyb.delay(10)')

    print('USR switch passed')

    ## accel test
    if True:
        print("hold level")
        pyb.exec('accel = pyb.Accel()')
        pyb.exec('while abs(accel.x()) > 10 or abs(accel.y()) > 10: pyb.delay(10)')

        print("tilt left")
        pyb.exec('while accel.x() > -10: pyb.delay(10)')
        pyb.exec('leds[0].on()')

        print("tilt forward")
        pyb.exec('while accel.y() < 10: pyb.delay(10)')
        pyb.exec('leds[1].on()')

        print("tilt right")
        pyb.exec('while accel.x() < 10: pyb.delay(10)')
        pyb.exec('leds[2].on()')

        print("tilt backward")
        pyb.exec('while accel.y() > -10: pyb.delay(10)')
        pyb.exec('leds[3].on()')

        print('accel passed')

    print('seconds since boot:', pyb.get_time())

    pyb.exec('apply(leds, lambda l:l.off())')

    pyb.exit_raw_repl()
    pyb.close()

def shell():
    pyb = Pyboard('/dev/ttyACM0')
    pyb.enter_raw_repl()

    def get_file_path(input_text):
        _, file_path = input_text.split(" ")
        file_path = file_path.strip("'\"")
        return file_path

    def print_help_function():
        print("""
    python: enter a mini python
    list: list files and folders
    sync: sync current folder file into pyboard
    upload "*.py": upload a file to pyboard
    delete "*.py": delete a file in pyboard
    """)

    print_help_function()

    def mini_python():
        print("")
        while True:
            command = input("> ").strip()
            if command == "exit()":
                break
            if "print(" in command:
                print(pyb.run(command) + "\n")
            else:
                print(pyb.eval(command).decode("utf-8", errors="ignore"))

    while True:
        command = input("\nyour command: ").strip()
        if command == "help":
            print_help_function()
        elif command == "python":
            mini_python()
        elif command == "list" or command == "ls":
            print(pyb.list_files_and_folders("."))
        elif command == "sync":
            pyboard.sync_folder("./", "/")
            print("done")
        elif command.startswith("cat "):
            file_path = get_file_path(command)
            print("\n")
            print(pyb.run("""
    with open("{name}", "r") as f:
        print(f.read())
    """.format(name=file_path)))
        elif command.startswith("upload "):
            file_path = get_file_path(command)
            pyb.upload_file(file_path, file_path)
            print("done")
        elif command.startswith("delete "):
            file_path = get_file_path(command)
            pyb.delete_file_or_folder(file_path)
            print("done")

    pyb.exit_raw_repl()


if __name__ == "__main__":
    #### there might at least have 2 bugs that causes the fire() function not working
    #from auto_everything.python import Python
    #py = Python()
    #py.fire2(Pyboard)

    shell()
