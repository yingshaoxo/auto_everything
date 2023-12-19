#!/usr/bin/env /usr/bin/python3
#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python3

# Run this to generate bash auto complete script: Tools -- --completion

import os, re
import random
import json
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
    def push(self, comment: str):
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

    def parse(self, url: str):
        #export accessToken=""
        if ("https://" in url):
            url = url[len("https://"):]
            accessToken = os.getenv('accessToken')
            result = f"git clone https://oauth2:{accessToken}@{url}"
            print(result)
            t.run(f'echo "{result}" | pbcopy')

    def commit(self, comment: str):
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
git submodule update --init --recursive
""")

    def merge_by_hand(self, branch_name: str):
        t.run(f"""
git merge --no-ff --no-commit origin/{branch_name}
""")

    def delete_branch(self, branch_name: str):
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

    def delete_git_big_git_file(self, filename: str):
        t.run(f"""
bfg --delete-files {filename}
""")

    def delete_macos_ds_store(self):
        files = disk.get_files(".", recursive=True)
        for file in files:
            if ".DS_Store" in file:
                try:
                    disk.delete_a_file(file)
                    print(f"file deleted: {file}")
                except Exception as e:
                    print(e)
            else:
                if disk.get_file_name(file).startswith("._"):
                    the_real_file_path = disk.join_paths(disk.get_directory_path(file), disk.get_file_name(file)[2:])
                    if disk.exists(the_real_file_path):
                        try:
                            disk.delete_a_file(file)
                            print(f"file deleted: {file}")
                        except Exception as e:
                            print(e)

    def sync_with_remote_git_repo(self, repo_url: str):
        t.run(f"""
# Add a new remote upstream repository
git remote add upstream {repo_url}
git remote set-url upstream {repo_url}

# Get upstream code
git fetch --all

# Sync 1
git checkout master && git merge upstream/master  --allow-unrelated-histories

# Sync 2
git checkout main && git merge upstream/main  --allow-unrelated-histories
        """)

    def add_remote_git_repo_url(self, repo_url: str):
        t.run(f"""
git remote set-url --add --push origin {repo_url}
        """)

    def git_abort(self):
        t.run(f"""
        git merge --abort
        """)

    def delete_sub_git_folder(self, path: str = "."):
        files = disk.get_folder_and_files(folder=path, recursive=True)
        files = [file.path for file in files if file.path.endswith("/.git")]
        files.sort(key=len)
        if len(files) > 0:
            files = files[1:]
        for file in files:
            file = disk.get_absolute_path(file)
            try:
                disk.delete_a_folder(file)
            except Exception as e:
                print(f"{file}: ", e)
                try:
                    disk.delete_a_file(file)
                except Exception as e2:
                    print(f"{file}: ", e2)
            print(f"Folder got deleted: {file}")
        print("done")

    def reset_storage_permission(self, path: str):
        if path != "/":
            t.run(f"""
            sudo chown -R $(whoami):$(whoami) {path}
            sudo chmod g+rw {path}
            """)

    def check_port(self, port:str | None=None):
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

    def repair_disk(self, disk_name: str=""):
        if disk_name != "":
            t.run(f"sudo umount {disk_name}")
            t.run(f"sudo fsck -p {disk_name}")
            print(f"\n\nsudo fsck {disk_name}")
        else:
            t.run(f"lsblk -p")
            t.run(f"df -hl")

    def pkill(self, name: str):
        t.kill(name)

    def find_port(self, port: str):
        t.run(f"""
            sudo lsof -i:{port}
            sudo ss -lptn 'sport = :{port}'
        """)

    def find_a_file_by_name(self, regex_expression: str):
        pwd = t.run_command('pwd') #print working directory
        t.run(f"find '{pwd}' -type f | grep '{regex_expression}'")

    def find_a_file_by_content_string(self, regex_expression: str):
        pwd = t.run_command('pwd')
        t.run(f"grep -r -e '{regex_expression}' '{pwd}'")

    def sync_folder_or_file(self, source: str, target: str):
        t.run(f"rsync -v --info=progress2 --partial '{source}' '{target}'")

    def show_space_usage(self, path: str | None):
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

    def my_shell(self, type: str | None=None):
        if type == "x":
            def command_line_transforming(command: str) -> str:
                return "proxychains4 " + command
        else:
            def command_line_transforming(command: str) -> str:
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

    def find_big_file(self, path: str = "."):
        t.run(f"""
        du -a -h --max-depth=1 {path} | sort -h
        """)

    def start_vnc_service(self, password: str="aaaaaaAAAAAA123456!!!!!!"):
        t.run(f"""
        sudo apt-get install x11vnc net-tools
        /usr/bin/x11vnc -passwd "{password}" -forever -rfbport 5900
        #sudo snap install novnc
        #novnc
        """)

    def clean_docker_garbage(self):
        t.run(f"""
        sudo docker container prune
        sudo docker image prune
        sudo docker system prune -a
        """)

    def fake_storage_backup(self, backup_file_path: str | None=None):
        saving_path = None
        if backup_file_path != None:
            saving_path = backup_file_path
        else:
            saving_path = "./fake_storage_backup.json"

        files = disk.get_folder_and_files(folder=".")
        data_list: list[Any] = []
        for file_or_folder in files:
            data_list.append({
                "path": file_or_folder.path,
                "type": 'folder' if file_or_folder.is_folder else 'file'
            })

        with open(saving_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(data_list, indent=4))
        print(f"fake backup is done, it is in: {saving_path}")

    def fake_storage_recover(self, storage_tree_json_file: str | None=None):
        if (storage_tree_json_file == None):
            storage_tree_json_file = "./fake_storage_backup.json"
            if not disk.exists(storage_tree_json_file):
                print("you need to give me a json file that was generated from 'fake_backup' function.")
                exit()

        with open(storage_tree_json_file, 'r', encoding='utf-8') as f:
            raw_json = f.read()
            json_object = json.loads(raw_json)

        for item in json_object:
            path = item['path']
            type = item['type']
            if type == 'folder':
                os.mkdir(path)
                print(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("")
                print(path)

        print("\nfake recover is done, sir.")

    def delete_git_and_gitignore_file(self):
        files = disk.get_gitignore_folders_and_files(".", also_return_dot_git_folder=True)
        for file in files:
            try:
                if disk.is_directory(file):
                    disk.delete_a_folder(file)
                else:
                    disk.delete_a_file(file)
                print(f"file/folder deleted: {file}")
            except Exception as e:
                print(e)

    def wake_up_the_light(self):
        from time import sleep
        while True:
            t.run(f'vlc --vout none /home/yingshaoxo/Documents/WakeUp.mp3 vlc://quit')
            sleep(21)

    def hi(self):
        self.help()

    def help(self):
        print(help(Tools))


py.make_it_global_runnable(executable_name="Tools")
py.fire2(Tools)
