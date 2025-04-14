from auto import terminal

def test_run():
    assert terminal.run("ls") == None

def test_run_command():
    assert terminal.run_command("uname") == "Linux\n"

def test_get_pids():
    assert len(terminal._get_pids()) > 0

def test_is_running():
    assert terminal.is_running("bash") == True
    assert terminal.is_running("asdfaskdflashdkakjkgdsagfjda") == False

def test_kill():
    command = "ping"
    terminal.run(f"{command} baidu.com &")
    assert terminal.is_running(command) == True
    terminal.kill(command)
    assert terminal.is_running(command) == False
