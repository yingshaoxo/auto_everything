from time import sleep
sleep(1)
# should check if the boot uploader pin is on or not, if it is on, stop everything and wait for upload the new_system.py


board_name = None

if board_name == None:
    try:
        import pyb
        del pyb
        board_name = "pyboard"
    except Exception as e:
        pass

if board_name == None:
    try:
        import rp2
        del rp2
        board_name = "pico"
    except Exception as e:
        pass

if board_name == None:
    try:
        from machine import Pin
        Pin(32, Pin.OUT, value=0)
        del Pin
        board_name = "esp32"
    except Exception as e:
        pass

if board_name == None:
    board_name = "unix"


try:
    if board_name == "pyboard":
        import main_pyboard_1_dot_1_plus
    elif board_name == "pico":
        #import main_pico
        #import system_launcher_pico
        import main_pico_core
    elif board_name == "esp32":
        import main_esp32
    elif board_name == "unix":
        import main_unix
except Exception as e:
    print(e)
    with open("log.txt", "w") as f:
        f.write(str(e))
