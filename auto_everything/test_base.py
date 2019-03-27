import os
import pexpect

# ------------------------
# ------------------------
# ------------------------
### Testing for IO


# ------------------------
# ------------------------
# ------------------------
### Testing for Terminal

from auto_everything.base import Terminal
t = Terminal()

def test_fix_path():
    path = "~/hi"

    result = t.fix_path(path, username="yingshaoxo")
    assert result == "/home/yingshaoxo/hi"

    result = t.fix_path(path)
    assert result == os.path.expanduser(path)

def test_run():
    pass

# ------------------------
# ------------------------
# ------------------------

if __name__ == "__main__":
    pass
