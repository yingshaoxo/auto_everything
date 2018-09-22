
import os
from auto_everything.base import IO, Python, Terminal
io = IO()


files = ' '.join(os.listdir('.'))
io.log(files)
        