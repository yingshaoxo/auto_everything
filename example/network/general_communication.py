import time
import sys
import os
import tempfile

from multiprocessing import Process, Manager, freeze_support
from auto_everything.network_ import General_Communication_System

temp_dir = tempfile.gettempdir()
the_file = os.path.join(temp_dir, "my_file_socket.txt")
print(the_file)

def computer_1_sending_function(communicator):
    sys.stdin = open(0)

    def start():
        if not os.path.exists(the_file):
            with open(the_file, "w") as f:
                f.write("")
    def write_zero():
        with open(the_file, "a") as f:
            f.write("0")
    def write_one():
        with open(the_file, "a") as f:
            f.write("1")
    def end():
        with open(the_file, "a") as f:
            f.write("\n")

    while True:
        input_string = input("computer_1: What you want to say?").strip() + "\n"
        input_data = input_string.encode("ascii")

        try:
            start()
            communicator.send(input_data, write_zero, write_one)
            end()
        except Exception as e:
            print(e)

def computer_2_receiving_function(communicator):
    global last_modification_time
    last_modification_time = None

    def get_input():
        global last_modification_time
        if not os.path.exists(the_file):
            with open(the_file, "w") as f:
                f.write("")

        if last_modification_time == None:
            last_modification_time = os.path.getmtime(the_file)
        while os.path.getmtime(the_file) == last_modification_time:
            time.sleep(0.1)
        last_modification_time = os.path.getmtime(the_file)

        with open(the_file, "r") as f:
            text = f.read()
        if len(text) > 0:
            with open(the_file, "w") as f:
                f.write("")
        for one in text:
            if one == "0":
                communicator.get_zero_input()
            elif one == "1":
                communicator.get_one_input()

    try:
        all_data = bytes()
        while True:
            get_input()
            data = communicator.receive()
            if len(data) > 0:
                all_data += data
                if all_data[-1:] == b"\n":
                    print(" From computer_2:", all_data)
                    all_data = bytes()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    finally:
        pass

if __name__ == "__main__":
    freeze_support()

    #manager = Manager()
    #global_dict = manager.dict()
    #udp_data_list = manager.list()

    communicator = General_Communication_System()

    process_list = []
    process_list.append(
        Process(target=computer_1_sending_function, args=(communicator,)),
    )
    process_list.append(
        Process(target=computer_2_receiving_function, args=(communicator,)),
    )

    for p in process_list:
        p.start()

    try:
        process_list[0].join()
    except KeyboardInterrupt:
        for p in process_list:
            if p.is_alive():
                p.terminate()
