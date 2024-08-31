from auto_everything.python import Python
from auto_everything.terminal import Terminal
py = Python()
terminal = Terminal(debug=True)

from dev_tools.ys_pyboard import Pyboard
pyboard = Pyboard("/dev/ttyACM0")

class Tools():
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

py.fire2(Tools)
