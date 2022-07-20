#!/usr/bin/env /Users/yingshaoxo/Library/Caches/pypoetry/virtualenvs/auto-everything-_Gc1gPdN-py3.10/bin/python
import os
from auto_everything.python import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal(debug=True)

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

    def forcepull(self):
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

    def hi(self):
        print("hi")


py.make_it_global_runnable(executable_name="Tools")
py.fire(Tools)
