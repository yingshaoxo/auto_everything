from auto import disk

def test_get_folders():
    assert "/home/yingshaoxo" in disk.get_folders("/home")
