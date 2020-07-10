from myx11 import MyX11
from PIL import Image
import numpy as np
from time import sleep

myx11 = MyX11()

width, height, data = myx11.capture_screen("pixel")
if width:
    print(width, height)
    data = np.array(data, np.uint8).reshape([height, width, 3])
    img = Image.fromarray(data, "RGB")
    img.show()
