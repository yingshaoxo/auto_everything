from auto_everything.network_ import Serial
from time import sleep
serial = Serial("/dev/ttyUSB0")

i = 0
while True:
    serial.write(b"Hi, " + str(i).encode(encoding="ascii"))
    sleep(2)

    i += 1
    if i > 999:
        i = 0


