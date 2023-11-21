#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
#!/usr/bin/env /Users/yingshaoxo/Library/Caches/pypoetry/virtualenvs/auto-everything-_Gc1gPdN-py3.10/bin/python

import os
import json
from typing import Any
from auto_everything.python import Python
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk

disk = Disk()
py = Python()
t = Terminal(debug=True)

saving_path = "./disk_fake_backup.txt"

def itIsWindows():
    if os.name == 'nt':
        return True
    return False

def get_folder_and_files(
    folder: str
):
    """
    Get files recursively under a folder.

    Parameters
    ----------
    folder: string
    recursive: bool
    """
    folder = disk._expand_user(folder)
    assert os.path.exists(folder), f"{folder} is not exist!"
    files: list[str] = []
    for root, dirnames, filenames in os.walk(folder):
        for dirname in dirnames:
            abs_folder_path = os.path.join(root, dirname)
            files.append(abs_folder_path)
        for filename in filenames:
            file = os.path.join(root, filename)
            if os.path.isfile(file):
                files.append(file)
    return files

class Tools():
    def test(self):
        files = get_folder_and_files(folder=".")
        for file in files:
            print(file)

    def fake_storage_backup(self, backup_file_path: str | None=None):
        saving_path = None
        if backup_file_path != None:
            saving_path = backup_file_path
        files = get_folder_and_files(folder=".")
        data_list: list[Any] = []
        for file_or_folder in files:
            data_list.append({
                "path": file_or_folder,
                "type": 'folder' if os.path.isdir(file_or_folder) else 'file'
            })
        if (saving_path != None):
            with open(saving_path, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_list, indent=4))
            print(f"fake backup is done, it is in: {saving_path}")

    def fake_storage_recover(self, storage_tree_json_file: str | None=None):
        if (storage_tree_json_file == None):
            print("you need to give me a json file that was generated from 'fake_backup' function.")
            exit()
        if not disk.exists(storage_tree_json_file):
            print(f"path wrong: {storage_tree_json_file}")
            exit()
        with open(storage_tree_json_file, 'r', encoding='utf-8') as f:
            raw_json = f.read()
            json_object = json.loads(raw_json)
        for item in json_object:
            path = item['path']
            type = item['type']
            if type == 'folder':
                os.mkdir(path)
                print(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("")
                print(path)
        print("\nfake recover is done, sir.")


py.make_it_global_runnable(executable_name="Disk")
py.fire(Tools)
