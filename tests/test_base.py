"""
import os
import time

from auto_everything.base import Terminal
from auto_everything.base import IO

# ------------------------
# ------------------------
# ------------------------
# Testing for Terminal
t = Terminal()

SHORT_DELAY = 1


def test_fix_path():
    path = "~/hi"

    result = t.fix_path(path, username="yingshaoxo")
    assert result == "/home/yingshaoxo/hi"

    result = t.fix_path(path)
    assert result == os.path.expanduser(path)


def test_run():
    command = "python3 -m http.server 1998"
    t.run(command, wait=False)
    time.sleep(SHORT_DELAY)
    assert t.is_running(command) == True
    t.kill(command)

    command = "python3 -m http.server 1998"
    t.run(command, cwd="~", wait=False)
    time.sleep(SHORT_DELAY)
    html = t.run_command("wget -qO- 127.0.0.1:1998")
    assert 'HTML' in html
    t.kill(command)

    command = "python3 -m http.server 1998"
    t.run(command, cwd=None, wait=False)
    time.sleep(SHORT_DELAY)
    html = t.run_command("wget -qO- 127.0.0.1:1998")
    assert os.listdir(t.current_dir)[0] in html
    t.kill(command)


def test_run_command():
    files = t.run_command("ls")
    assert len(files) > 0


def test_run_program():
    command = "python3 -m http.server 1998"
    t.run_program(command, cwd="~")
    time.sleep(SHORT_DELAY)
    html = t.run_command("wget -qO- 127.0.0.1:1998")
    assert 'HTML' in html
    t.kill(command)

def test_exists():
    t.run_command("mkdir yingshaoxo_is_somebody")
    assert t.exists("yingshaoxo_is_somebody") is True
    t.run_command("rm yingshaoxo_is_somebody -r")
    assert t.exists("yingshaoxo_is_somebody") is False


# ------------------------
# ------------------------
# ------------------------
# Testing for IO
io = IO()


def test_write_and_read_and_append():
    file_path = "temp.yingshaoxo.xyz"

    io.write(file_path, "something")
    assert io.read(file_path) == "something"

    io.append(file_path, "right")
    assert "right" in io.read(file_path)

    t.run_command("rm temp.yingshaoxo.xyz")


def test_write_and_read_settings():
    io.write_settings("fuck", "you")
    assert io.read_settings("fuck", "me") == "you"

    io.empty_settings()
    assert io.read_settings("fuck", "me") == "me"

    io.empty_settings()


if __name__ == "__main__":
    command = "python3 -m http.server 1998"
    t.run(command, wait=False)
    time.sleep(1)
    print(t.is_running("python3 -m http.server 1998"))
    while 1:
        pass
"""
