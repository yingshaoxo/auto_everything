#!/usr/bin/env /usr/bin/python3
#!/usr/bin/env /home/python/use_docker_to_build_static_python3_binary_executable/data/Python-3.10.4/python
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
    def push(self, comment):
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
            t.run("""
            git config --global user.name "leo.wooyj"
            git config --global user.email "leo.wooyj@finpoints.com"
            #"yingjie.hu@fargowealth.com.hk"

            git add .
            git commit -m "{comment}"
            git push origin
            """.format(comment=comment))
        else:
            t.run("""
            git config --global user.name "yingshaoxo"
            git config --global user.email "yingshaoxo@gmail.com"

            git add .
            git commit -m "{comment}"
            git push origin
            """.format(comment=comment))
            return

    def parse(self, url):
        #export accessToken=""
        if ("https://" in url):
            url = url[len("https://"):]
            accessToken = os.getenv('accessToken')
            result = "git clone https://oauth2:{accessToken}@{url}".format(accessToken=accessToken)
            print(result)
            t.run('echo "{result}" | pbcopy'.format(result=result))

    def commit(self, comment):
        if "/CS/" in t.run_command("pwd"):
            t.run("""
            git config --global user.name "yingshaoxo"
            git config --global user.email "yingshaoxo@gmail.com"
            git add .
            git commit -m "{comment}"
            #git push origin
            """.format(comment=comment))
        else:
            t.run("""
            git config --global user.name "yingjie.hu"
            git config --global user.email "yingjie.hu@fargowealth.com.hk"
            git add .
            git commit -m "{comment}"
            #git push origin
            """.format(comment=comment))

    def force_push(self):
        branch = "master"
        for s in t.run_command("git branch").split("\n"):
            if "*" in s:
                branch = s.replace("*", "").strip()
        t.run("""
git push origin {branch} --force
""".format(branch=branch))

    def force_pull(self):
        branch = "master"
        for s in t.run_command("git branch").split("\n"):
            if "*" in s:
                branch = s.replace("*", "").strip()
        t.run("""
git fetch --all
git reset --hard origin/{branch}
git submodule update --init --recursive
""".format(branch=branch))

    def merge_by_hand(self, branch_name):
        t.run("""
git merge --no-ff --no-commit origin/{branch_name}
""".format(branch_name=branch_name))

    def delete_branch(self, branch_name):
        t.run("""
git push origin --delete {branch_name}
""".format(branch_name=branch_name))

    def undo_commit(self):
        # there has a bug related to "~", the run will replace '~' into '/home/username'
        command = """
git reset --mixed HEAD~1
"""
        t.run(command)
        print("\n\n\ntry:\n" + command)

    def undo_changes(self):
        t.run("""
git reset --hard HEAD^
""")

    def git_difference(self):
        t.run("""
git status
git status -s
""")
        print("\nGet more information by using: git diff")

    def delete_git_big_git_file(self, filename):
        t.run("""
bfg --delete-files {filename}
""".format(filename=filename))

    def delete_macos_ds_store(self):
        files = disk.get_files(".", recursive=True)
        for file in files:
            if ".DS_Store" in file:
                try:
                    disk.delete_a_file(file)
                    print("file deleted: {file}".format(file=file))
                except Exception as e:
                    print(e)
            else:
                if disk.get_file_name(file).startswith("._"):
                    the_real_file_path = disk.join_paths(disk.get_directory_path(file), disk.get_file_name(file)[2:])
                    if disk.exists(the_real_file_path):
                        try:
                            disk.delete_a_file(file)
                            print("file deleted: {file}".format(file=file))
                        except Exception as e:
                            print(e)

    def delete_pyc_and_pycache(self):
        files = disk.get_files(".", recursive=True)
        for file in files:
            if file.endswith(".pyc"):
                try:
                    disk.delete_a_file(file)
                    print("file deleted: {file}".format(file=file))
                except Exception as e:
                    print(e)

        files = disk.get_folders(".", recursive=True)
        for file in files:
            if file.endswith("__pycache__"):
                try:
                    disk.delete_a_folder(file)
                    print("folder deleted: {file}".format(file=file))
                except Exception as e:
                    print(e)

    def sync_with_remote_git_repo(self, repo_url):
        t.run("""
# Add a new remote upstream repository
git remote add upstream {repo_url}
git remote set-url upstream {repo_url}

# Get upstream code
git fetch --all

# Sync 1
git checkout master && git merge upstream/master  --allow-unrelated-histories

# Sync 2
git checkout main && git merge upstream/main  --allow-unrelated-histories
        """.format(repo_url=repo_url))

    def add_remote_git_repo_url(self, repo_url):
        t.run("""
git remote set-url --add --push origin {repo_url}
        """.format(repo_url=repo_url))

    def git_abort(self):
        t.run("""
        git merge --abort
        """)

    def delete_sub_git_folder(self, path = "."):
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
                print(file, ": ", e)
                try:
                    disk.delete_a_file(file)
                except Exception as e2:
                    print(file, ": ", e2)
            print("Folder got deleted: {file}".format(file=file))
        print("done")

    def reset_storage_permission(self, path):
        if path != "/":
            t.run("""
            sudo -S chown -R $(whoami):$(whoami) {path}
            sudo -S chmod g+rw {path}
            """.format(path=path))

    def check_port(self, port=None):
        if port == None:
            t.run("sudo -S ss -antpl")
        else:
            t.run("sudo -S netstat -nlp | grep :{port}".format(port=port))

    '''
    def image_compress(self, image=""):
        if image != "":
            t.run(f"""
    convert {image} -sampling-factor 4:2:0 -strip -quality 85 -adaptive-resize 60% -interlace JPEG -colorspace RGB compressed_{image}
            """)  # -gaussian-blur 0.05
    '''

    def repair_disk(self, disk_name=""):
        if disk_name != "":
            t.run("sudo -S umount {disk_name}".format(disk_name=disk_name))
            t.run("sudo -S fsck -p {disk_name}".format(disk_name=disk_name))
            print("\n\nsudo fsck {disk_name}".format(disk_name=disk_name))
        else:
            t.run("lsblk -p")
            t.run("df -hl")

    def pkill(self, name):
        t.kill(name)

    def find_port(self, port):
        t.run("""
            sudo -S lsof -i:{port}
            sudo -S ss -lptn 'sport = :{port}'
        """.format(port=port))

    def find_a_file_by_name(self, regex_expression):
        pwd = t.run_command('pwd') #print working directory
        t.run("find '{pwd}' -type f | grep '{regex_expression}'".format(pwd=pwd, regex_expression=regex_expression))

    def find_a_file_by_content_string(self, regex_expression):
        pwd = t.run_command('pwd')
        t.run("grep -r -e '{regex_expression}' '{pwd}'".format(regex_expression=regex_expression, pwd=pwd))

    def show_space_usage(self, path="./"):
        if path == None:
            path = t.run_command('pwd')
        #path = os.path.abspath(path)

        folder_size_text = t.run_command("du -hl -d 1 '{path}'".format(path=path))
        splits = folder_size_text.split("\n")
        folder_size_text = "\n".join(splits[:-1])
        total_size_line = splits[-1].strip(". ")

        file_size_text = t.run_command("ls -p -ahl '{path}' | grep -v /".format(path=path))
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

    def show_file_tree(self, level = None):
        if level == None:
            level = 1
        elif level < 1:
            level = 1
        t.run("""
        tree -L {level}
        """.format(level=level))
        # files = disk.get_folder_and_files(folder=".")
        # pprint(list(files))

    def find_big_file_and_folders(self, path = ".", level=2):
        t.run("""
        du -a -h --max-depth={level} {path} | sort -h
        """.format(level=level, path=path))

    def start_vnc_service(self, password="aaaaaaAAAAAA123456!!!!!!"):
        t.run("""
        sudo -S apt-get install x11vnc net-tools
        /usr/bin/x11vnc -passwd "{password}" -forever -rfbport 5900
        #sudo snap install novnc
        #novnc
        """.format(password=password))

    def clean_docker_garbage(self):
        t.run("""
        sudo -S docker container prune
        sudo -S docker image prune
        sudo -S docker system prune -a
        """)

    def fake_storage_backup(self, backup_file_path=None):
        saving_path = None
        if backup_file_path != None:
            saving_path = backup_file_path
        else:
            saving_path = "./fake_storage_backup.json"

        files = disk.get_folder_and_files(folder=".")
        data_list = []
        for file_or_folder in files:
            data_list.append({
                "path": file_or_folder.path,
                "type": 'folder' if file_or_folder.is_folder else 'file',
                "size": '0' if file_or_folder.is_folder else str(disk.get_file_size(file_or_folder.path)),
            })
        data_list.sort(key=lambda item: (item["path"], item["type"], item["size"]))

        with open(saving_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(data_list, indent=4))
        print("fake backup is done, it is in: {saving_path}".format(saving_path=saving_path))

    def fake_storage_recover(self, storage_tree_json_file=None):
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

    def delete_git_and_gitignore_file(self, target_folder=None, also_delete_git_folder=True):
        """
        Current git has problems with historical big data.
        They should create a function that deletes everything that inside .gitignore in history record
        So the final git folder could be very small
        """
        if target_folder == None:
            target_folder = "./"

        files = disk.get_gitignore_folders_and_files(target_folder, also_return_dot_git_folder=also_delete_git_folder)
        #print(files)
        #exit()
        for file in files:
            try:
                if disk.is_directory(file):
                    disk.delete_a_folder(file)
                else:
                    disk.delete_a_file(file)
                print("file/folder deleted: {file}".format(file=file))
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
                    print("file/folder deleted: {file}".format(file=file))
                except Exception as e:
                    print(e)

    def save_code_repository_to_yingshaoxo_disk(self, a_code_folder="./"):
        a_code_folder = disk.get_absolute_path(a_code_folder)
        if a_code_folder and disk.exists(a_code_folder):
            base_yingshaoxo_disk_code_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code/"
            folder_name = disk.get_directory_name(a_code_folder)
            if folder_name == "":
                print("something is wrong")
                exit()
            target_code_folder = base_yingshaoxo_disk_code_folder + folder_name

            print("source_folder:", a_code_folder)
            print("target_folder:", target_code_folder)
            input("Does it looks fine for you? If so, hit enter.")

            disk.delete_a_folder(target_code_folder)
            disk.copy_a_folder(a_code_folder, target_code_folder, use_gitignore_file=True)
            #self.delete_git_and_gitignore_file(target_folder=target_code_folder, also_delete_git_folder=True)

    def wake_up_the_light(self):
        while True:
            t.run('vlc --vout none /home/yingshaoxo/Documents/WakeUp.mp3 vlc://quit')
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

        t.run("""
            ffmpeg -i '{video_path}' -c:v libx264 -vf "scale={resolution}:flags=neighbor" -r 23.98 -b:v {kb_limit} -c:a copy '{target_path}'
        """.format(video_path=video_path, resolution=resolution, kb_limit=kb_limit, target_path=target_path))
        #ffmpeg -i input.mp4 -c:v libx264 -vf scale=640:360 -r 23.98 -b:v 498k -c:a aac -b:a 128k output.mp4

    def compress_video2(self, video_path, target_path):
        t.run("""
            ffmpeg -i '{video_path}' -c:v libx264 -vf "scale=320:trunc(ow*ih/iw/2)*2:flags=neighbor" -r 23.98 -b:v 100k -c:a copy '{target_path}'
        """.format(video_path=video_path, target_path=target_path))

    def compress_video_to_fake_480p(self, video_path, target_path):
        t.run("""
            ffmpeg -i '{video_path}' -vf "scale=480:trunc(ow*ih/iw/2)*2:sws_flags=neighbor" '{target_path}'
        """.format(video_path=video_path, target_path=target_path))

    def cut_video(self, video_path, target_path, start_time, end_time):
        """
        start_time or end_time: '01:02' means 1 minute 2 seconds
        """
        t.run("""
            ffmpeg -i '{video_path}' -ss {start_time} -to {end_time} -c copy '{target_path}'
        """.format(video_path=video_path, start_time=start_time, end_time=end_time, target_path=target_path))

    def get_audio_from_video(self, video_path, audio_path):
        t.run("""
            ffmpeg -i '{video_path}' '{audio_path}'
            """.format(video_path=video_path, audio_path=audio_path)
        )

    def get_images_from_video(self, video_path, image_folder):
        image_folder = image_folder.rstrip("/")
        t.run("""
            mkdir '{image_folder}'
            ffmpeg -i '{video_path}' '{image_folder}/%d.png'
        """.format(image_folder=image_folder, video_path=video_path))
        video_info = t.run_command("ffmpeg -i '{video_path}'".format(video_path=video_path))
        lines = [line for line in video_info.split("\n") if " fps" in line]
        print("\n".join(lines))

    def convert_images_to_video(self, image_folder, video_path, frame_rate=None):
        image_folder = image_folder.rstrip("/")
        if frame_rate == None:
            t.run("""
                ffmpeg -f image2 -i '{image_folder}/%d.png' '{video_path}'
            """.format(image_folder=image_folder, video_path=video_path))
        else:
            t.run("""
                ffmpeg -framerate {frame_rate} -i '{image_folder}/%d.png' '{video_path}'
            """.format(frame_rate=frame_rate, image_folder=image_folder, video_path=video_path))

    def merge_audio_and_video(self, video_path, audio_path, target_path):
        t.run("""
            ffmpeg -i '{video_path}' -i '{audio_path}' -c:v copy -c:a copy '{target_path}'
        """.format(video_path=video_path, audio_path=audio_path, target_path=target_path))

    def compress_audio(self, audio_path, target_path, kbps=128):
        t.run("""
            ffmpeg -i '{audio_path}' -b:a {kbps}k '{target_path}'
        """.format(audio_path=audio_path, kbps=kbps, target_path=target_path))

    def record_screen(self, target_path):
        t.run("""
            ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0 '{target_path}'
        """.format(target_path))

        """
        # record with sound
        ffmpeg -sources
        ffmpeg -f pulse -i alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source -f x11grab -r 30 -s 1920x1080 -i :0 -ac 2 -async 25 -filter_complex amix=inputs=1 output.mp4
        """

    def check_battery_power(self):
        t.run("""
        cat /sys/class/power_supply/BAT0/capacity
        """)

    def check_cpu_frequency(self):
        t.run("""
        watch -n.1 "grep 'MHz' /proc/cpuinfo"
        """)
        #apt install tlp
        #systemctl enable tlp

    def change_brightness(self, value="400"):
        t.run("""
        echo {value} | tee /sys/class/backlight/intel_backlight/brightness
        """.format(value=value))

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
        print("""
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
        """.format(interface=interface))

    def serve(self, port, single_threading=False, pure_index_page=True):
        #from auto_everything.http_ import Yingshaoxo_Threading_Based_Http_Server, Yingshaoxo_Http_Request
        from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request
        from time import sleep

        """
        @dataclass()
        class Yingshaoxo_Http_Request():
            socket_connection: Any
            socket_address: Any

            context: Any
            host: str
            method: str
            url: str
            url_arguments: dict[str, str]
            headers: dict[str, str]
            payload: dict[str, Any] | None
        """

        if pure_index_page == "True":
            pure_index_page = True
        if pure_index_page == "False":
            pure_index_page = False

        def home_handler(request):
            try:
                real_file_path = "." + request.url
                if os.path.isdir(real_file_path):
                    files = os.listdir("." + request.url)

                    if ("index.html" not in files) or (pure_index_page == True):
                        folders = [file for file in files if "." not in file]
                        files = [file for file in files if "." in file]

                        folders.sort()
                        files.sort()

                        all_list = folders + files
                        new_request_url = request.url.strip("/")
                        if new_request_url != "":
                            new_request_url = "/" + new_request_url

                        new_all_list = []
                        for file in all_list:
                            target_path = new_request_url + "/" + file
                            if os.path.isdir("." + target_path):
                                target_path += "/"
                                new_all_list.append('<a href="{the_path}">{file}</a>'.format(the_path=target_path, file=file))
                            else:
                                new_all_list.append('<a href="{the_path}">{file}</a>'.format(the_path=target_path, file=file))
                        all_list = new_all_list

                        html_code = "<br>".join(all_list)
                        html_code = '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + html_code
                    else:
                        with open(os.path.join(real_file_path, "index.html"), "r") as f:
                            html_code = f.read()

                    if single_threading == False:
                        return html_code, {"Accept-Ranges": "bytes"}
                    else:
                        return html_code
                else:
                    if single_threading != False:
                        with open(real_file_path, "rb") as f:
                            bytes_data = f.read()
                        return bytes_data

                    full_size = os.path.getsize(real_file_path)
                    if "Range" not in request.headers:
                        with open(real_file_path, "rb") as f:
                            bytes_data = f.read()
                        return_headers = {"Accept-Ranges": "bytes"}
                        if real_file_path.endswith(".css"):
                            return_headers["content-type"] = "text/css"
                        elif real_file_path.endswith(".js"):
                            return_headers["content-type"] = "text/javascript"
                        elif real_file_path.endswith(".htm"):
                            return_headers["content-type"] = "text/html"
                        elif real_file_path.endswith(".md") or real_file_path.endswith(".txt"):
                            return_headers["content-type"] = "text/plain"
                        elif real_file_path.endswith(".json"):
                            return_headers["content-type"] = "application/json"
                        elif real_file_path.endswith(".pdf"):
                            return_headers["content-type"] = "application/pdf"
                        elif real_file_path.endswith(".xml"):
                            return_headers["content-type"] = "text/xml"
                        elif real_file_path.endswith(".gif"):
                            return_headers["content-type"] = "image/gif"
                        elif real_file_path.endswith(".png"):
                            return_headers["content-type"] = "image/png"
                        elif real_file_path.endswith(".jpg") or real_file_path.endswith(".jpeg"):
                            return_headers["content-type"] = "image/jpeg"
                        return bytes_data, return_headers
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
                        return bytes_data, {"Accept-Ranges": "bytes", "Content-Range": "bytes {start}-{end}/{full_size}".format(start=str(start_bytes), end=str(end_bytes), full_size=full_size)}, "HTTP/1.1 206 Partial Content"
            except Exception as e:
                print(e)
                first_line = "HTTP/1.1 404 "
                return "", {}, first_line+str(e)

        def special_handler(request):
            return "Hello, world, fight for personal freedom."

        router = [
            [r"/__yingshaoxo__", special_handler],
            [r"(.*)", home_handler]
        ]

        yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
        #yingshaoxo_http_server = Yingshaoxo_Threading_Based_Http_Server(router=router)
        yingshaoxo_http_server.start(host = "0.0.0.0", port = int(port))

    def find_string(self, search_string, start_from=0):
        t.run("grep -R '{}'".format(search_string))
        print()

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

    def code_helper(self, old=False):
        if old != False:
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

                        class_lines = [line for line in list(reversed(the_lines[:found_index])) if line.strip().startswith("class ")]
                        if len(class_lines) > 0:
                            print(class_lines[0] + "\n")

                        print(next_text.strip("`"))
                        break
                if found_index == None:
                    print("\n\n_______\n\n")
                    print("I can't find anything.")
        else:
            from auto_everything.ml import Yingshaoxo_Text_Completor
            yingshaoxo_text_completor = Yingshaoxo_Text_Completor()
            from auto_everything.disk import Disk
            disk = Disk()

            type_limiter = [".txt", ".midi_txt", ".md", ".py", ".h", ".c", ".cpp", ".js", ".cjs", ".ts", ".vue", ".sh", ".html", ".scss", ".css", ".json", ".proto", ".dart", ".go", ".yaml", ".php", ".rs", ".toml", ".cc", ".yml", ".lua", ".htm", ".vim", ".hero", ".java", ".sql_command", ".kt", ".CPP", ".less", ".cs"]
            #type_limiter = [".txt", ".midi_txt", ".md", ".py", ".h", ".c", ".js", ".sh", ".html", ".proto", ".dart", ".go", ".vim", ".hero", ".java", ".kt"]
            #type_limiter = [".txt", ".md", ".py", ".sh"]
            files = disk.get_files("./", True, type_limiter=type_limiter)
            source_text = ""
            for file_path in files:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    source_text += text + "\n\nxxx___xxx\n\n"

            while True:
                input_text = input("What you want to know: ")
                response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=612, level=64, complete_how_many_character_for_each_time=None)
                if response:
                    response = response.split("\n\nxxx___xxx\n\n")[0]
                    print("Result: \n\n" + input_text + response)
                    print("\n\n_______\n\n")

    def connect_android(self):
        print("""
Do following:

sudo apt install adb fastboot
rm -fr ~/.android/
adb kill-server
adb devices
adb shell
        """)

    def rsync(self, from_path, to_path, ignore_folder="None"):
        # example: /usr/bin/Tools rsync ./Core/ /media/yingshaoxo/disk2_data/Yingshaoxo_Data/Core/ "Additional/Game/"

        # from could be a folder or file, to could be a folder or file 
        # there would only folder to folder sync and file to file sync
        # but the rsync logic sucks, so here the python should try to fix it
        # here we will be calling the rsync software, because it sync stuff when need, not copy the whole things
        # The following works, but it require me in the right folder, which is not what I want. Can we use absolute path?
        # rsync -avzR --delete --progress "./Yingshaoxo_Data" "/media/yingshaoxo/The Atlantis/"
        if os.path.isfile(from_path) and os.path.isdir(to_path):
            raise ValueError("Cannot sync file to directory - append filename to destination")
        if os.path.isdir(from_path) and os.path.isfile(to_path):
            raise ValueError("Cannot sync directory to file path")

        abs_from = os.path.abspath(from_path)
        abs_to = os.path.abspath(to_path)

        if os.path.isdir(from_path):
            os.chdir(abs_from)

            command_line = [
                "rsync",
                "-avzR",  # -R preserves relative path structure
                "--delete",
                "--progress",
                "--size-only",
                # "--dry-run", # check file changes but not doing anything
                '"./"',
                '"{}"'.format(abs_to),
            ]
            if ignore_folder != "None":
                if type(ignore_folder) == str:
                    command_line.insert(4, "--exclude '{}'".format(ignore_folder))

            print(command_line)
            command_line = " ".join(command_line)
            command_line = 'cd "{}"\n'.format(abs_from) + command_line

            t.run(command_line, cwd=abs_from)
        else:
            print("Do not support file yet.")

    def hi(self):
        self.help()

    def help(self):
        print(help(Tools))


py.make_it_global_runnable(executable_name="Tools")
py.fire2(Tools)
