import os
import pexpect
import time

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

SHORT_DELAY = 0.1

def test_fix_path():
    path = "~/hi"

    result = t.fix_path(path, username="yingshaoxo")
    assert result == "/home/yingshaoxo/hi"

    result = t.fix_path(path)
    assert result == os.path.expanduser(path)

def test_run():
    command = "python3 -m http.server 1998"
    t.run(command, wait=False)
    assert t.is_running(command) == True
    t.kill(command)

    command = "python3 -m http.server 1998"
    t.run(command, cwd="~", wait=False)
    time.sleep(SHORT_DELAY)
    html = t.run_command("wget -qO- 127.0.0.1:1998")
    assert 'Downloads' in html
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
    assert 'Downloads' in html
    t.kill(command)

# ------------------------
# ------------------------
# ------------------------

if __name__ == "__main__":
    pass
