from auto_everything.disk import Disk
disk = Disk()

from io import BytesIO
import os

from pprint import pprint

def test_get_bytesio():
    result = disk.get_bytesio_from_a_file(__file__)
    assert type(result) == BytesIO

def test_get_files():
    gitignore_text = """
    *.py
    """
    files = disk.get_files(".", gitignore_text=gitignore_text)
    for file in files:
        assert not file.endswith(".py")

def test_get_folder_and_files():
    files = disk.get_folder_and_files(".")
    for index, file in enumerate(files):
        #print(file.path, file.level, file.folder, file.name, file.is_file, file.is_folder)
        assert file.level == 1
        if index > 1:
            break

def test_get_folder_and_files_tree():
    folder = "."
    root = disk.get_folder_and_files_tree(folder=folder, type_limiter=[".py"])
    assert root.children != None and len(root.children) != 0