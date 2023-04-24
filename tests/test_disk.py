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

def test_compress():
    blackhole_folder = "/Users/yingshaoxo/CS/auto_everything/blackhole"
    zip_target_path = disk.join_paths(blackhole_folder, "hi.zip")

    disk.compress(
        input_folder_path="/Users/yingshaoxo/CS/auto_everything/auto_everything",
        output_zip_path=zip_target_path
    )
    assert disk.exists(zip_target_path) 

def test_uncompress():
    blackhole_folder = "/Users/yingshaoxo/CS/auto_everything/blackhole"
    zip_target_path = disk.join_paths(blackhole_folder, "hi.zip")

    target_path = disk.join_paths(blackhole_folder, "hi.zip")
    output_folder = disk.join_paths(blackhole_folder, "uncompressed")
    disk.uncompress(compressed_file_path=target_path, extract_folder_path=output_folder)
    assert disk.exists(output_folder) 

def test_get_temp_folder_path():
    print(disk.get_a_temp_folder_path())