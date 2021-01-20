```
from auto_everything.camera import FakeCamera
import time
import numpy as np

# two frame
blue = np.zeros((480,640,3), dtype=np.uint8)
blue[:,:,2] = 255
red = np.zeros((480,640,3), dtype=np.uint8)
red[:,:,0] = 255

# create fake camera
fakecam = FakeCamera()

# keep running
while True:
    fakecam.next(red)
    time.sleep(1/30.0)

    fakecam.next(blue)
    time.sleep(1/30.0)
```
