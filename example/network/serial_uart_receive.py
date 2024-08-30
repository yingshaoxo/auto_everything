from auto_everything.network_ import Serial
from time import sleep

serial1 = Serial("/dev/ttyUSB1", timeout=0.1)
while True:
    result = serial1.read()
    if len(result) == 0:
        sleep(1)
    else:
        print(result)
