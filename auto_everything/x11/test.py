import myx11
from PIL import Image
import numpy as np
from time import sleep

#a = myx11.a_cpp_function()
#print(a)

#print(myx11.window_exists("final"))

#width, height, data = myx11.capture_screen("x11")
#if width:
#    print(width, height)
#    data = np.array(data, np.uint8).reshape([height, width, 3])
#    img = Image.fromarray(data, "RGB")
#    img.show()

print(myx11.press_a_key("piXel"))
