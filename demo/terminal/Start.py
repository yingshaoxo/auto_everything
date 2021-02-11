#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal
from auto_everything.gui import Controller

py = Python()
t = Terminal()
controller = Controller()


class Mission():
    def _kill(self):
        t.kill("jupyter-lab")
        t.kill("kernel")
        t.kill("pycharm")
        t.kill("code/code")
        t.kill("nautilus")
        t.kill("xournalpp")
        t.kill("evince")
        t.kill("chrome")
        t.kill("obs")

    def play(self):
        controller.write("cd ~/CS/notebooks")
        controller.press("enter")
        self._kill()
        t.run("""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate cling

cd ~/CS/notebooks
nohup jupyter-lab . &
google-chrome "https://leetcode.com/problemset/all/"
                """, wait=False)

    def lab(self):
        controller.write("cd ~/CS/notebooks")
        controller.press("enter")
        self._kill()
        t.run("""
cd ~/CS/notebooks
nohup jupyter-lab . &
google-chrome "https://translate.google.com/" &
google-chrome "https://keras.io/examples/" &
        """, wait=False)

    def ui(self):
        path = "~/CS/freedom/2021"
        controller.write(f"cd {path}")
        controller.press("enter")

        self._kill()
        t.run(f"""
        google-chrome "https://translate.google.com/" &
        google-chrome "https://google.com" &
        #terminator --working-directory="{path}"
        nohup xournalpp "~/CS/freedom/2021/Dev Plans.xopp" &
        cd {path}
        xdg-open .
        code freedom
        """, wait=False)

    def py(self):
        path = "~/CS/auto_everything"
        controller.write(f"cd {path}")
        controller.press("enter")

        self._kill()
        t.run_command(f"""
        google-chrome "https://google.com" &
        #terminator --working-directory="{path}"
        cd {path}
        nohup pycharm-community &
        nohup xournalpp "~/CS/auto_everything/plans.xopp" &
        """)

    def math(self):
        path = "/home/yingshaoxo/Documents/01.高数"
        controller.write(f"cd {path}")
        controller.press("enter")
        self._kill()
        t.run("""
google-chrome "https://app.gitbook.com/@yingshaoxo/s/advanced-mathematics-notes/han-shu-de-lian-xu-xing-yu-ji-xian-function-continuity-and-limit/qiu-ji-xian-de-fang-fa" &

#xdg-open /home/yingshaoxo/Downloads/SYNC/Resources/Books/Math
xdg-open "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/2021考研数学张宇基础30讲【适用基础班讲义】 .pdf"
xdg-open "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/[解析册] 2021张宇1000题（数学一）无水印.pdf"

nohup xournalpp "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/2021考研数学张宇基础30讲【适用基础班讲义】 .pdf" &
nohup xournalpp "/home/yingshaoxo/Downloads/SYNC/Resources/Books/Math/[试题册] 2021张宇1000题（数学一）无水印.pdf" &
        """)

    def record(self):
        path = "~/Videos"
        controller.write(f"cd {path}")
        controller.press("enter")

        self._kill()
        t.run("""
        xdg-open ~/Videos/doing &
        #terminator --working-directory="~/Videos" &
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
