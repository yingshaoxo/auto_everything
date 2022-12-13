from auto_everything.disk import Disk
disk = Disk()

from io import BytesIO

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