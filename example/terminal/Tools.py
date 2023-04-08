#!/usr/bin/env /root/.cache/pypoetry/virtualenvs/auto-everything-ovpo7K6j-py3.10/bin/python
#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
#!/usr/bin/env /Users/yingshaoxo/Library/Caches/pypoetry/virtualenvs/auto-everything-_Gc1gPdN-py3.10/bin/python

# Run this to generate bash auto complete script: Tools -- --completion

import os, re
import random
from auto_everything.python import Python
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk

from pprint import pprint

py = Python()
t = Terminal(debug=True)
disk = Disk()

def itIsWindows():
    if os.name == 'nt':
        return True
    return False

class Tools():
    def push(self, comment):
        if "/Work/" in t.run_command("pwd"):
            t.run(f"""
            git config --global user.name "leo.wooyj"
            git config --global user.email "leo.wooyj@finpoints.com" 
            #"yingjie.hu@fargowealth.com.hk"

            git add .
            git commit -m "{comment}"
            git push origin
            """)
        else:
            t.run(f"""
            git config --global user.name "yingshaoxo"
            git config --global user.email "yingshaoxo@gmail.com"

            git add .
            git commit -m "{comment}"
            git push origin
            """)
            return

    def parse(self, url):
        #export accessToken=""
        if ("https://" in url):
            url = url[len("https://"):]
            accessToken = os.getenv('accessToken')
            result = f"git clone https://oauth2:{accessToken}@{url}"
            print(result)
            t.run(f'echo "{result}" | pbcopy')

    def commit(self, comment):
        if "/CS/" in t.run_command("pwd"):
            t.run(f"""
            git config --global user.name "yingshaoxo"
            git config --global user.email "yingshaoxo@gmail.com"
            git add .
            git commit -m "{comment}"
            #git push origin
            """)
        else:
            t.run(f"""
            git config --global user.name "yingjie.hu"
            git config --global user.email "yingjie.hu@fargowealth.com.hk"
            git add .
            git commit -m "{comment}"
            #git push origin
            """)
    
    def force_push(self):
        branch = "master"
        for s in t.run_command("git branch").split("\n"):
            if "*" in s:
                branch = s.replace("*", "").strip()
        t.run(f"""
git push origin {branch} --force 
""")

    def force_pull(self):
        branch = "master"
        for s in t.run_command("git branch").split("\n"):
            if "*" in s:
                branch = s.replace("*", "").strip()
        t.run(f"""
git fetch --all
git reset --hard origin/{branch}
""")

    def merge_by_hand(self, branch_name):
        t.run(f"""
git merge --no-ff --no-commit origin/{branch_name}
""")

    def delete_branch(self, branch_name):
        t.run(f"""
git push origin --delete {branch_name}
""")

    def undo_commit(self):
        t.run("""
git reset --mixed HEAD~1
""")

    def undo_changes(self):
        t.run("""
git reset --hard HEAD^
""")

    def delete_git_file(self, filename):
        t.run(f"""
bfg --delete-files {filename}
""")

    def abort(self, comment):
        t.run(f"""
        git merge --abort
        """)

    def reset_permission(self, path):
        if path != "/":
            t.run(f"""
            sudo chown -R $(whoami):$(whoami) {path}
            sudo chmod g+rw {path}
            """)

    def check(self, port=None):
        if port == None:
            t.run(f"sudo ss -antpl")
        else:
            t.run(f"sudo netstat -nlp | grep :{port}")

    '''
    def image_compress(self, image=""):
        if image != "":
            t.run(f"""
    convert {image} -sampling-factor 4:2:0 -strip -quality 85 -adaptive-resize 60% -interlace JPEG -colorspace RGB compressed_{image}
            """)  # -gaussian-blur 0.05
    '''

    def repair_disk(self, disk_name=""):
        if disk_name != "":
            t.run(f"sudo umount {disk_name}")
            t.run(f"sudo fsck -p {disk_name}")
            print(f"\n\nsudo fsck {disk_name}")
        else:
            t.run(f"lsblk -p")
            t.run(f"df -hl")

    def pkill(self, name):
        t.kill(name)
    
    def find_port(self, port):
        t.run(f"""
            lsof -i:{port}
        """)

    def find(self, regex_expression):
        pwd = t.run_command('pwd') #print working directory
        t.run(f"find '{pwd}' -type f | grep '{regex_expression}'")

    def find_string(self, regex_expression):
        pwd = t.run_command('pwd')
        t.run(f"grep -r -e '{regex_expression}' '{pwd}'")

    def get_non_app_launch_items(self):
        items = t.run_command("launchctl list").split("\n")
        new_items = []
        for item in items:
            if "\tcom.apple." not in item:
                new_items.append(item.strip().replace("\t", "    "))
        pprint(new_items)

    def remove_the_stupid_macos_launch_item(self, service_name):
        print("yeah, macos is stupid!")
        t.run(f"launchctl bootout gui/501/{service_name}")

    def show_space_usage(self, path):
        if path == None:
            path = t.run_command('pwd')
        #path = os.path.abspath(path)

        folder_size_text = t.run_command(f"du -hl -d 1 '{path}'")
        splits = folder_size_text.split("\n")
        folder_size_text = "\n".join(splits[:-1])
        total_size_line = splits[-1].strip(". ")

        file_size_text = t.run_command(f"ls -p -ahl '{path}' | grep -v /")
        splits = file_size_text.split("\n")[1:]
        splits = ["     ".join(re.split(r"\s+", line)[4:][::2][::2]) for line in splits]
        file_size_text = "\n".join(splits)

        print(folder_size_text + "\n\n" + file_size_text + "\n\nTotal Size: " + total_size_line)

    def update_go_dependencies(self):
        t.run("""
        go get -d -u -t ./...
        go mod tidy
        """)
    
    def my_shell(self, type=None):
        if type == "x":
            def command_line_transforming(command):
                return "proxychains4 " + command
        else:
            def command_line_transforming(command):
                return command

        t.debug = False
        print("Welcome!\n\nLet's begin the journey by type your command here:\n")
        print("> ", end="")
        while True:
            try:
                command = input("")
                t.run(command_line_transforming(command=command))
                print()
                print("> ", end="")
            except Exception as e:
                print(e)

    def where_to_go(self):
        places = [
            "5-KFC",
            "5-McDonald's",
            "4-Charger_Space_Left",
            "4-Charger_Space_Right",
            "2-KFC",
            "2-7-family_Left",
            "2-7-family_Right",
            "1-7-family",
        ]
        print(random.choice(places))

    def show_file_tree(self, level:int | None = None):
        if level == None:
            level = 1
        elif level < 1:
            level = 1
        t.run(f"""
        tree -L {level}
        """)
        # files = disk.get_folder_and_files(folder=".")
        # pprint(list(files))

    def hi(self):
        self.help()

    def help(self):
        print(help(Tools))


py.make_it_global_runnable(executable_name="Tools")
py.fire(Tools)
