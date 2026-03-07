import time

from auto_everything.disk import Disk
disk = Disk()

from auto_everything.audio_ import Audio
audio = Audio()

if not disk.exists("/home/yingshaoxo/Downloads/song_small.binary"):
    audio = audio.read_from_file("/home/yingshaoxo/Downloads/song.wav")
    audio.save_to_simple_binary_audio("/home/yingshaoxo/Downloads/song_small.binary")

import serial
usb_serial = serial.Serial("/dev/ttyUSB0", baudrate=115200)

# need to let it play with stable speed, 8k/s.
start_time = time.time()
point_counting = 0
with open("/home/yingshaoxo/Downloads/song_small.binary", "rb") as f:
    while True:
        data = f.read(1)
        point_counting += 1
        if not data:
            break
        time_use = time.time() - start_time
        time_should_use = point_counting / 8000
        while time_use < time_should_use:
            time_use = time.time() - start_time
        usb_serial.write(data)

print("done")
