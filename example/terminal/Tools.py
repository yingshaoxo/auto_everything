#!/usr/bin/env /usr/bin/python3
#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python3
# Run this to generate bash auto complete script: Tools -- --completion

import os, re
import random
import json
from time import sleep
from pprint import pprint

from auto_everything.python import Python
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk

py = Python()
t = Terminal(debug=True)
disk = Disk()

def itIsWindows():
    if os.name == 'nt':
        return True
    return False

class Tools():
    def push(self, comment: str):
        urls = t.run_command("git remote -v")
        if "git@gitlab.com:" not in urls:
            print("You should also transfer your project to gitlab")
            print("You can do it by using: ")
            print("    git remote set-url --add --push origin {gitlab_repo_url}")
            ok = input("\n\nIgnore and go on?(y/n)").strip()
            if ok == 'y' or ok == None or ok == "":
                pass
            else:
                exit()

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
            sudo -S chown -R $(whoami):$(whoami) {path}
            sudo -S chmod g+rw {path}
            """)

    def check_port(self, port:str | None=None):
        if port == None:
            t.run(f"sudo -S ss -antpl")
        else:
            t.run(f"sudo -S netstat -nlp | grep :{port}")

    '''
    def image_compress(self, image=""):
        if image != "":
            t.run(f"""
    convert {image} -sampling-factor 4:2:0 -strip -quality 85 -adaptive-resize 60% -interlace JPEG -colorspace RGB compressed_{image}
            """)  # -gaussian-blur 0.05
    '''

    def repair_disk(self, disk_name: str=""):
        if disk_name != "":
            t.run(f"sudo -S umount {disk_name}")
            t.run(f"sudo -S fsck -p {disk_name}")
            print(f"\n\nsudo fsck {disk_name}")
        else:
            t.run(f"lsblk -p")
            t.run(f"df -hl")

    def pkill(self, name: str):
        t.kill(name)

    def find_port(self, port: str):
        t.run(f"""
            sudo -S lsof -i:{port}
            sudo -S ss -lptn 'sport = :{port}'
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

    def find_big_file_and_folders(self, path: str = ".", level=2):
        t.run(f"""
        du -a -h --max-depth={level} {path} | sort -h
        """)

    def start_vnc_service(self, password: str="aaaaaaAAAAAA123456!!!!!!"):
        t.run(f"""
        sudo -S apt-get install x11vnc net-tools
        /usr/bin/x11vnc -passwd "{password}" -forever -rfbport 5900
        #sudo snap install novnc
        #novnc
        """)

    def clean_docker_garbage(self):
        t.run(f"""
        sudo -S docker container prune
        sudo -S docker image prune
        sudo -S docker system prune -a
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

    def delete_git_and_gitignore_file(self, also_delete_git_folder=True):
        """
        Current git has problems with historical big data.
        They should create a function that deletes everything that inside .gitignore in history record
        So the final git folder could be very small
        """
        files = disk.get_gitignore_folders_and_files(".", also_return_dot_git_folder=also_delete_git_folder)
        for file in files:
            try:
                if disk.is_directory(file):
                    disk.delete_a_folder(file)
                else:
                    disk.delete_a_file(file)
                print(f"file/folder deleted: {file}")
            except Exception as e:
                print(e)

        answer = input("Done.\n\nWant to do a deeper scan and deletion to delete more? (y/n)")
        if "y" in answer:
            files = disk.get_gitignore_folders_and_files_by_using_yingshaoxo_method(".", also_return_dot_git_folder=also_delete_git_folder)
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
        while True:
            t.run(f'vlc --vout none /home/yingshaoxo/Documents/WakeUp.mp3 vlc://quit')
            sleep(21)

    def compress_video(self, video_path, target_path, use_720p=None, use_1080p=None, special=None):
        resolution = "640:360"
        kb_limit = "498k"
        if use_720p == "True":
            resolution = "1280:720"
            kb_limit = "747k"
        elif use_1080p == "True":
            resolution = "1920:1080"
            kb_limit = "1120k"

        if special != None:
            resolution = "1920:1080"
            kb_limit = "1992k"

        t.run(f"""
            ffmpeg -i '{video_path}' -c:v libx264 -vf scale={resolution} -r 23.98 -b:v {kb_limit} -c:a copy '{target_path}'
        """)
        #ffmpeg -i input.mp4 -c:v libx264 -vf scale=640:360 -r 23.98 -b:v 498k -c:a aac -b:a 128k output.mp4

    def compress_video2(self, video_path, target_path):
        t.run(f"""
            ffmpeg -i '{video_path}' -c:v libx264 -vf "scale=320:180" -r 23.98 -b:v 100k -c:a copy '{target_path}'
            #ffmpeg -i '{video_path}' -c:v libx264 -vf scale=320:180 -r 16 -b:v 100k -c:a copy '{target_path}'
        """)

    def cut_video(self, video_path, target_path, start_time, end_time):
        """
        start_time or end_time: '01:02' means 1 minute 2 seconds
        """
        t.run(f"""
            ffmpeg -i '{video_path}' -ss {start_time} -to {end_time} -c copy '{target_path}'
        """)

    def get_audio_from_video(self, video_path, audio_path):
        t.run(f"""
            ffmpeg -i '{video_path}' '{audio_path}'
        """)

    def get_images_from_video(self, video_path, image_folder):
        image_folder = image_folder.rstrip("/")
        t.run(f"""
            mkdir '{image_folder}'
            ffmpeg -i '{video_path}' '{image_folder}/%d.png'
        """)
        video_info = t.run_command(f"ffmpeg -i '{video_path}'")
        lines = [line for line in video_info.split("\n") if " fps" in line]
        print("\n".join(lines))

    def convert_images_to_video(self, image_folder, video_path, frame_rate=None):
        image_folder = image_folder.rstrip("/")
        if frame_rate == None:
            t.run(f"""
                ffmpeg -f image2 -i '{image_folder}/%d.png' '{video_path}'
            """)
        else:
            t.run(f"""
                ffmpeg -framerate {frame_rate} -i '{image_folder}/%d.png' '{video_path}'
            """)

    def merge_audio_and_video(self, video_path, audio_path, target_path):
        t.run(f"""
            ffmpeg -i '{video_path}' -i '{audio_path}' -c:v copy -c:a copy '{target_path}'
        """)

    def compress_audio(self, audio_path, target_path, kbps=128):
        t.run(f"""
            ffmpeg -i '{audio_path}' -b:a {kbps}k '{target_path}'
        """)

    def check_battery_power(self):
        t.run(f"""
        cat /sys/class/power_supply/BAT0/capacity
        """)

    def check_cpu_frequency(self):
        t.run(f"""
        watch -n.1 "grep 'MHz' /proc/cpuinfo"
        """)
        #apt install tlp
        #systemctl enable tlp

    def change_brightness(self, value="400"):
        t.run(f"""
        echo {value} | tee /sys/class/backlight/intel_backlight/brightness
        """)

    def connect_wifi(self):
        info = t.run_command("iwconfig")
        print(info)
        interface = "wlan0"
        for one in [one.strip() for one in info.split("\n") if one.strip()!=""]:
            if one.startswith("w"):
                interface = one.split()[0]
                break
        print("\n\nDo the following yourself:\n\n")
        sleep(3)
        print(f"""
sudo vi /etc/network/interfaces
# add following code to the bottom

#audo lo
#iface lo inet loopback

auto {interface}
allow-hotplug {interface}
iface {interface} inet dhcp
    iface {interface} inet dhcp
    wpa-ssid "<wifi_name>"
    wpa-psk "<password>"

# execute another command
sudo apt install ifupdown
ifdown -v {interface}; ifup -v {interface}

# if above not work, try reboot or ethernet wire connection, wifi is not reliable. new linux, especially ubuntu23+ is shit. if you rename /usr/bin/python3 to something else, you'll never be able to connect to new wifi.
# use ubuntu version 16 or lower is fine.
# if you have to use apt to install ifdown or ifup, it means that package can get modified by ubuntu at any time, which means the syntax of /etc/network/interfaces also got changed, which means this method is not working any more. I still remember ubuntu removes ifconfig linux command. now have to use "ip address" to get your host ip, which means ubuntu function is not stable. Let's say fuck to newer version of ubuntu, because they sucks.
        """)

    def serve(self, port):
        #from auto_everything.http_ import Yingshaoxo_Threading_Based_Http_Server, Yingshaoxo_Http_Request
        from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request
        from time import sleep

        """
        @dataclass()
        class Yingshaoxo_Http_Request():
            context: Any
            host: str
            method: str
            url: str
            url_arguments: dict[str, str]
            headers: dict[str, str]
            payload: dict[str, Any] | None
        """

        def home_handler(request):
            try:
                real_file_path = "." + request.url
                if os.path.isdir(real_file_path):
                    files = os.listdir("." + request.url)

                    folders = [file for file in files if "." not in file]
                    files = [file for file in files if "." in file]

                    folders.sort()
                    files.sort()

                    all_list = folders + files
                    new_request_url = request.url.lstrip("/")
                    if new_request_url != "":
                        new_request_url = "/" + new_request_url
                    all_list = [f'<a href="{new_request_url}/{file}">{file}</a>' for file in all_list]

                    html_code = "<br>".join(all_list)
                    return html_code, {"Accept-Ranges": "bytes"}
                else:
                    full_size = os.path.getsize(real_file_path)
                    if "Range" not in request.headers:
                        with open(real_file_path, "rb") as f:
                            bytes_data = f.read()
                        return bytes_data, {"Accept-Ranges": "bytes"}
                    else:
                        range = request.headers["Range"]
                        range_data = range.split("=")[1]
                        start_bytes, end_bytes = range_data.split("-")
                        if start_bytes != "":
                            start_bytes = int(start_bytes)
                        if end_bytes != "":
                            end_bytes = int(end_bytes)
                        else:
                            end_bytes = full_size
                        with open(real_file_path, "rb") as f:
                            f.seek(start_bytes)
                            bytes_data = f.read(end_bytes-start_bytes)
                        return bytes_data, {"Accept-Ranges": "bytes", "Content-Range": f"bytes {str(start_bytes)}-{str(end_bytes)}/{full_size}"}, "HTTP/1.1 206 Partial Content"
            except Exception as e:
                print(e)
                return str(e)

        def special_handler(request: Yingshaoxo_Http_Request):
            return "Hello, world, fight for personal freedom."

        router = {
            r"/__yingshaoxo__": special_handler,
            r"(.*)": home_handler
        }

        yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
        yingshaoxo_http_server.start(host = "0.0.0.0", port = int(port))

    def find_string(self, search_string, start_from=0):
        start_from = int(start_from)
        files = disk.get_files(folder="./", recursive=True, use_gitignore_file=True)
        counting = 0
        for file in files:
            try:
                with open(file, "r") as f:
                    text = f.read()
                lines = text.split("\n")
                found_index = None
                for index, line in enumerate(lines):
                    if search_string in line and line.strip()[0] not in ["#", '"', "'", "/"]:
                        found_index = index
                        break
                if found_index != None:
                    if counting >= start_from:
                        next_text = "\n".join(lines[found_index:found_index + 20])
                        print("file path: " + file)
                        print("content: \n\n" + next_text)
                        return
                    counting += 1
            except Exception as e:
                pass
        print("not found")

    def code_helper(self):
        documentation = py.generate_documentation_for_a_python_project("./", "/tmp/doc.md", just_return_string=True)
        parts = documentation.split("\n\n_______\n\n")

        previous_input_text = None
        start_from = 0
        while True:
            input_text = input("\n\n_______\n\nWhat you want to search? (n for next)\n").strip()
            if len(input_text) != 1:
                previous_input_text = input_text
                start_from = 0
            else:
                start_from += 1
                if previous_input_text == None:
                    continue
                input_text = previous_input_text
            os.system("clear")

            counting = 0
            found_index = None
            the_lines = None
            for part in parts:
                if input_text in part:
                    lines = part.split("\n")
                    for index, line in enumerate(lines):
                        if input_text in line and line.strip()[0] not in ["#", '"', "'"]:
                            if counting >= start_from:
                                found_index = index
                                the_lines = lines
                                break
                            counting += 1
                if found_index != None:
                    next_text = "\n".join(the_lines[found_index:found_index + 20])
                    print("\n\n_______\n\n")
                    print(next_text.strip("`"))
                    break
            if found_index == None:
                print("\n\n_______\n\n")
                print("I can't find anything.")

    def hi(self):
        self.help()

    def help(self):
        print(help(Tools))


py.make_it_global_runnable(executable_name="Tools")
py.fire2(Tools)
