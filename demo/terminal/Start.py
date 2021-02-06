#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal()


class Mission():
    def play(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")
        t.run("""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate cling

cd ~/CS/notebooks
nohup jupyter-lab . &
google-chrome "https://leetcode.com/problemset/all/"
                """, wait=False)

    def lab(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")
        t.run("""
cd ~/CS/notebooks
nohup jupyter-lab . &
google-chrome "https://translate.google.com/" &
google-chrome "https://keras.io/examples/" &
        """, wait=False)

    def ui(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")
        path = "~/CS/freedom/2021"
        t.run(f"""
        google-chrome "https://translate.google.com/" &
        google-chrome "https://google.com" &
        #terminator --working-directory="{path}"
        nohup "xournalpp ~/CS/freedom/2021/Dev Plans.xopp" &
        cd {path}
        xdg-open .
        code freedom
        """, wait=False)

    def py(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")
        path = "~/CS/auto_everything"
        t.run(f"""
        google-chrome "https://google.com" &
        #terminator --working-directory="{path}"
        cd {path}
        nohup pycharm-community &
        """)

    def math(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")
        t.run("""
google-chrome "https://app.gitbook.com/@yingshaoxo/s/advanced-mathematics-notes/han-shu-de-lian-xu-xing-yu-ji-xian-function-continuity-and-limit/qiu-ji-xian-de-fang-fa" &

#xdg-open /home/yingshaoxo/Downloads/SYNC/Resources/Books/Math
xdg-open "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/2021考研数学张宇基础30讲【适用基础班讲义】 .pdf"
xdg-open "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/[解析册] 2021张宇1000题（数学一）无水印.pdf"

nohup xournalpp "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/2021考研数学张宇基础30讲【适用基础班讲义】 .pdf" &
nohup xournalpp "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/[试题册] 2021张宇1000题（数学一）无水印.pdf" &
        """)

    def record(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("obs")
        t.kill("chrome")
        t.run("""
        xdg-open ~/Videos/doing &
        terminator --working-directory="~/Videos" &
        obs-studio
        """, wait=False)

    def pi(self):
        t.run("""
terminator -e "ssh pi@192.168.49.17"
        """)

    def server(self):
        t.run("""
terminator -e "ssh root@149.28.229.110"
        """)

    def android(self):
        t.run("""
cd ~/Android/Sdk/emulator/bin64
emulator @Pixel_3a_API_30_x86 -no-snapshot-load
        """)

    def night(self):
        t.run("""
xcalib -s 0 -invert -alter
        """)

    def day(self):
        t.run("""
xcalib -c
        """)


py.fire(Mission)
py.make_it_global_runnable(executable_name="Start")
