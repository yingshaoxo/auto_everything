import unittest
import time

from auto_everything.base import IO, OS, Python, Terminal
io = IO()
_os = OS()
py = Python()
t = Terminal()

from auto_everything.math import Password
passwd = Password("yingshaoxo")


io.make_sure_sudo_permission()
print('\n' * 30)


class TestIO(unittest.TestCase):
    def test_basic_io(self):
        path = "log"
        io.write(path, "")
        self.assertEqual(io.read(path), "")

        io.log("hi")
        self.assertIn("hi", io.read(path))


class TestTerminal(unittest.TestCase):
    def test_fix_path(self):
        origin = "~/Codes"
        result = t.fix_path(origin)
        self.assertEqual("/", result[:1])

    def test_run_commands(self):
        r = t.run_command("ls")
        self.assertIn(".py", r)

    def test_run(self):
        p = t.run("top", wait=False)
        p.kill()

    def test_run_py(self):
        python = """
import os
from auto_everything.base import IO, Python, Terminal
io = IO()


files = ' '.join(os.listdir('.'))
io.log(files)
        """
        io.write('hi.py', python)
        t.run_command("rm log")
        t.run_py('hi.py', wait=True)
        self.assertIn(".py", io.read("log"))

    def test_run_sh(self):
        sh = """
echo "python" >> log
        """
        io.write('hi.sh', sh)

        t.run_command("rm log")
        t.run_sh('hi.sh', wait=True)
        self.assertIn("python", io.read("log"))

    def test_passwd(self):
        self.assertIn("A", passwd.update("hihihi"))

    def test_install(self):
        _os.uninstall_package('curl', force=True)
        self.assertIn('No such', t.run_command('curl'))
        _os.install_package('curl', force=True)
        self.assertIn('curl --help', t.run_command('curl'))

unittest.main()
