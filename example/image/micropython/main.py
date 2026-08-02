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

use_sd_card_system = False
try:
    #with open("configuration.txt", "r") as f:
    #    configuration_text = f.read()
    #if "use_sd_card_system = True" in configuration_text:
    #    use_sd_card_system = True
    if board_name == "pico":
        from machine import Pin, SPI
        import os
        import sdcard # use 'from machine import SDCard; import vfs' will raise problems. the SD card I am using is a 2GB one with fat16 format. maybe fat32 will work, similar to pyboard
        spi = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
        sd = sdcard.SDCard(spi,Pin(13))
        print("mounting...")
        os.mount(sd,"/")
        print(os.listdir("/"))
        print("Done")
        use_sd_card_system = True
except Exception as e:
    print(e)


try:
    if board_name == "pyboard":
        import main_pyboard_1_dot_1_plus
    elif board_name == "pico":
        if use_sd_card_system == True:
            import main
        else:
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
