from auto_everything.disk import Disk 
from pathlib import Path
import os
from pprint import pprint

from auto_everything.base import Terminal, OS
t = Terminal(debug=True)
os_ = OS()

disk = Disk()


class Network():
    def __init__(self):
        assert "not found" not in t.run_command("wget"), '''
'wget' is required for this module to work
You can install it with `sudo apt install wget`'''

    def download(self, url: str, target: str, size: str = "0B") -> bool:
        target = Path(target).expanduser().absolute()
        directory = target.parent
        assert os.path.exists(directory), f"target directory '{directory}' is not exits"
        t.run(f"wget {url} -O {target}")

        number = int("".join([i for i in list(size) if i.isdigit()]))
        unit = size.replace(str(number), "")
        assert unit in ["B", "KB", "MB"], f"number={number}, unit={unit}\nsize error, it should be 700B, 5KB, 40MB and so on."
        the_file_size = disk.get_file_size(target, unit)
        if (the_file_size > number):
            return True
        else:
            return False


if __name__ == "__main__":
    net = Network()
    result = net.download("https://github.com/yingshaoxo/My-books/raw/master/Tools.py", "~/.auto_everything/hi.txt")
    print(result)
