#!/usr/bin/env /home/yingshaoxo/Documents/static_python3.10.4_i386_or_i32_or_x86/python
#!/usr/bin/env /home/python/use_docker_to_build_static_python3_binary_executable/data/Python-3.10.4/python
from auto_everything.python import Python
from auto_everything.terminal import Terminal
py = Python()
terminal = Terminal(debug=True)

from dev_tools.ys_pyboard import Pyboard, exec_a_file, shell
pyboard = Pyboard("/dev/ttyACM0")

class Tools():
    def monitor(self):
        pyboard.read_forever_and_print()

    def shell(self):
        shell(pyboard)

    def run(self, file_path):
        exec_a_file(pyboard, file_path)

    def stop(self):
        pyboard.enter_raw_repl()
        pyboard.exit_raw_repl()
        print("cut power off can make it stop")

    def list_files(self):
        pyboard.enter_raw_repl()
        indent = "    "
        def print_tree(level, a_path):
            try:
                files = pyboard.list_files_and_folders(a_path)
            except Exception as e:
                print(e)
                return
            print(level*indent + a_path)
            for file in files:
                if "." not in file:
                    print_tree(level+1, a_path + "/" + file)
                else:
                    print(level*indent + a_path + "/" + file)
        print_tree(0, ".")
        pyboard.exit_raw_repl()

    def upload_current_folder(self):
        pyboard.enter_raw_repl()
        print("Old files:")
        print(pyboard.list_files_and_folders("."))
        print("\n\n")
        print("New files:")
        pyboard.sync_folder("./", "/")
        print("done")
        pyboard.exit_raw_repl()

    def upload_a_file(self, file_path):
        pyboard.enter_raw_repl()
        pyboard.upload_file(file_path, file_path)
        print("done")
        pyboard.exit_raw_repl()

    def delete_a_file(self, file_path):
        pyboard.enter_raw_repl()
        pyboard.delete_file_or_folder(file_path)
        print("done")
        pyboard.exit_raw_repl()

    def get_a_file_content(self, file_path):
        pyboard.enter_raw_repl()
        print(pyboard.run("""
with open("{name}", "r") as f:
    print(f.read())
    """.format(name=file_path)))
        pyboard.exit_raw_repl()


py.make_it_global_runnable(executable_name="pyboard")
Tools().shell()
#py.fire2(Tools)
