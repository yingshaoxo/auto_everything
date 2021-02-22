from auto import terminal

def test_run():
    assert terminal.run("ls") == None

def test_run_command():
    assert terminal.run_command("uname") == "Linux\n"

def test_get_pids():
    assert len(terminal.get_pids()) > 0
