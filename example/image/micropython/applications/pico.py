#terminal_arguments, input_char_=input_char, print_char_=print_char, input_=input, print_=print, real_print_=real_print, display_=display, run_command_=run_shell_command

#terminal_arguments = "cat soft_spi.py"
#terminal_arguments = "run_code print(1+1)"
#terminal_arguments = "list"
#terminal_arguments = "run fuck.py"
#terminal_arguments = "upload test.py"
#terminal_arguments = "delete test.py"
#real_print_ = print

import os
import os_path as path
import time

now_we_are_in_micropython = False
try:
    from machine import UART, Pin
    serial_uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    now_we_are_in_micropython = True
except Exception as e:
    print(e)
    pass

if now_we_are_in_micropython:
    def serial_read(number=None):
        if number == None:
            return serial_uart.read()
        return serial_uart.read(number)
    
    def serial_write(data):
        return serial_uart.write(data)

    def serial_read_until(min_num_bytes, ending, timeout=9):
        data = serial_read(min_num_bytes)
        if data == None:
            data = b""
        timeout_count = 0
        while True:
            temp_data = serial_read()
            if temp_data != None:
                data = data + temp_data
                time.sleep(0.01)
            elif data.endswith(ending):
                break
            else:
                timeout_count += 1
                if timeout_count >= 10 * timeout:
                    break
                time.sleep(0.1)
        return data

    def enter_raw_interpreter():
        # if you do not want to enter the raw shell, you use '\r' to end the input, it treats '\r' as enter key. '\r' == 0x0D, '\n' == 0x0A.
        # but I think you must use raw mode, others won't work well
        # after you get into raw_mode, every input ends with 0x04. but there has no print by default. and for the output, it always starts with '0x4F 0x4B', ends with '0x0D' or '0x04' or '0x3E'. and you should remove all 0x04 from output after first parsing.
        serial_write(b'\r\x03') # ctrl-C: interrupt any running program
        serial_write(b'\r\x01') # ctrl-A: enter raw REPL
        serial_write(b'\x04') # ctrl-D: soft reset
        # the real command is 0x0D, 0x03, 0x0D, 0x01, 0x04
        data = serial_read_until(1, b'to exit\r\n>')
        # final result match rule is: starts with '0x4F,0x4B', ends with '0x0D' or '0x04'.
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            print(data)
            raise Exception('could not enter raw repl')

    def serial_exec(command):
        command_bytes = command.encode("utf-8")
        for i in range(0, len(command_bytes), 32):
            serial_write(command_bytes[i:min(i+32, len(command_bytes))])
            time.sleep(0.01)
        serial_write(b'\x04')
        data = serial_read_until(1, b'\x04>')
        if not data.endswith(b'\x04>'):
            #print(data)
            raise Exception('timeout waiting for EOF reception')
        if data.startswith(b'Traceback') or data.startswith(b'  File '):
            #print(data)
            raise Exception('command failed')
        return data[2:-2]

    def serial_run(code):
        result = serial_exec(code)
        if result.endswith(b"\r\n\x04"):
            result = result[:-3]
        return result.decode("utf-8")

    def serial_execfile(filename):
        with open(filename) as f:
            pyfile = f.read()
        return serial_run(pyfile)

    def list_files_and_folders(folder_path="./"):
        script_content = """
import os
print(os.listdir("{folder_path}"))
        """.strip().format(
            folder_path=folder_path,
        )
        data_string = serial_run(script_content)
        start_index = data_string.find("[")
        return data_string[start_index:].replace("\',", "\',\n")

    def fs_writefile(dest, data, chunk_size=256):
        serial_exec("f=open('%s','wb')\nw=f.write" % dest)
        while data:
            chunk = data[:chunk_size]
            serial_exec("w(" + repr(chunk) + ")")
            data = data[len(chunk) :]
        serial_exec("f.close()")

    def upload_file(source_file_path, target_file_path):
        if not path.exists(source_file_path):
            raise Exception("File not exists: {}".format(source_file_path))
        if not path.isfile(source_file_path):
            return

        a_file = open(source_file_path, "rb")
        bytes_data = a_file.read()
        a_file.close()

        script_content = """
try:
    from gc import collect
    collect()
except Exception as e:
    pass

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
            folder_path=path.dirname(target_file_path)
        )
        serial_exec(script_content)
        fs_writefile(target_file_path, bytes_data, chunk_size=256)
        return

        script_content = """
the_bytes_list = [{int_byte_list_string}]

a_file = open("{file_path}", "wb")
a_file.write(bytes(the_bytes_list))
a_file.close()
        """.strip().format(
            int_byte_list_string=",".join([str(one) for one in bytes_data]),
            file_path=target_file_path,
            folder_path=path.dirname(target_file_path)
        )
        serial_exec(script_content)

    def delete_file_or_folder(target_file_path):
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
        serial_exec(script_content)

    def get_file_path(input_text):
        _, file_path = input_text.split(" ")
        file_path = file_path.strip("'\"")
        return file_path

    # the main function
    enter_raw_interpreter()

    command = terminal_arguments
    if command == "":
        real_print_("""
list: list files and folders

run "*.py": run a file from computer
run_code xxx: run code

upload "*.py": upload a file to pyboard
delete "*.py": delete a file in pyboard
cat "*.py": check a file
        """.strip() + "\n")
    elif command.startswith("run_code"):
        code = command[8:].strip()
        output = serial_run(code)
        real_print_("\n" + output + "\n")
    elif command.startswith("run"):
        file_path = get_file_path(command)
        output = serial_execfile(file_path)
        real_print_("\n" + output + "\n")
    elif command == "list" or command == "ls":
        real_print_(list_files_and_folders("."))
    elif command.startswith("cat "):
        file_path = get_file_path(command)
        real_print_(serial_run("""
with open("{name}", "r") as f:
    print(f.read())
""".format(name=file_path)))
    elif command.startswith("upload "):
        file_path = get_file_path(command)
        upload_file(file_path, file_path)
        real_print_("\n" + "done" + "\n")
    elif command.startswith("delete "):
        file_path = get_file_path(command)
        delete_file_or_folder(file_path)
        real_print_("\n" + "done" + "\n")
