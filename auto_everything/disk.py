from typing import List
from pathlib import Path
import os

from auto_everything.base import Terminal
t = Terminal(debug=True)


class Disk():
    def __init__(self):
        pass

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def get_files(self, folder: str, recursive: bool = True):
        assert os.path.exists(folder), f"{path} is not exist!"
        if recursive == True:
            files = []
            for root, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    if os.path.isfile(file):
                        files.append(file)
        else:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files

    def sort_files_by_time(self, files: List[str], reverse: bool = False):
        files.sort(key=os.path.getmtime, reverse=reverse)
        return files

    def get_file_size(self, path: str, level: str = "B") -> int:
        file = Path(path)
        assert file.exists(), f"{path} is not exist!"
        bytes = file.stat().st_size
        if (level == "B"):
            return int('{:,.0f}'.format(bytes))
        elif (level == "MB"):
            return int('{:,.0f}'.format(bytes/float(1 << 20)))
        elif (level == "KB"):
            return int('{:,.0f}'.format(bytes/float(1 << 10)))

    def uncompress(self, path: str, folder: str = None) -> bool:
        assert self.exists(path), f"{path} was not exist"
        t.run(f"rm {folder} -fr")
        t.run(f"mkdir -p {folder}")
        assert self.exists(folder), f"{folder} was not exit"
        try:
            suffix = Path(path).suffix
            if suffix == ".zip":
                t.run(f"unzip '{path}' -d '{folder}'")
                if len(os.listdir(folder)) == 1:
                    t.run(f"cd '{folder}' && cd * && mv * .. -f")
            elif suffix == ".gz":
                t.run(f"tar zxfv '{path}' '{folder}' --strip-components=1")
            if len(os.listdir(folder)):
                return True
            else:
                return False
        except Exception as e:
            raise e


if __name__ == "__main__":
    from pprint import pprint
    disk = Disk()
    files = disk.get_files(os.path.abspath(".."))
    files = disk.sort_files_by_time(files)
    pprint(files)
