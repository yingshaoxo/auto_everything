from auto import disk
from auto import terminal


def test_get_folders():
    assert "/home/yingshaoxo" in disk.get_folders("/home")

def test_write_string_to_a_file():
    path = "hi.txt"
    text = "you\nare\ngood"
    disk.write_string_to_file(text, path)
    what_we_get = disk.read_file_as_string(path)
    assert text == what_we_get
    terminal.run(f"rm {path}")
