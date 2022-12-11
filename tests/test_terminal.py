from auto_everything.base import Terminal

# ------------------------
# ------------------------
# ------------------------
# Testing for Terminal
t = Terminal()

def test_fix_path():
    path = """
    nohup xournalpp "~/CS/auto_everything/plans.xopp" &
    """.strip()

    assert t.fix_path(path) == """
    nohup xournalpp "/home/yingshaoxo/CS/auto_everything/plans.xopp" &
    """.strip()

def test_fix_path_with_username_provided():
    path = """
    nohup xournalpp "~/CS/auto_everything/plans.xopp" &
    """.strip()

    assert t.fix_path(path, username="ys") == """
    nohup xournalpp "/home/ys/CS/auto_everything/plans.xopp" &
    """.strip()

def test_pid_functions():
    a_command = "ping baidu.com"

    t.run_program(a_command)
    assert t.is_running(a_command) == True

    t.kill(a_command)
    assert t.is_running(a_command) == False
