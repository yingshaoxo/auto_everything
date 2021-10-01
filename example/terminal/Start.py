#!/usr/bin/env /usr/local/opt/python@3.9/bin/python3.9
#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal
from auto_everything.gui import Controller

py = Python()
t = Terminal()
controller = Controller()


class Mission():
    def _kill(self):
        process = [
            "jupyter-lab /home/yingshaoxo/CS",
            "kernel",
            # "pycharm",
            # "code/code",
            "nautilus",
            "xournalpp",
            "evince",
            # "chrome",
            "obs",
            "inkscape",
            "clion",
            "firefox",
            "screenkey",
        ]
        for p in process:
            t.kill(p)

    def _go_to(self, path):
        controller.write(f"cd {path}")
        controller.press("enter")

    def worklog(self):
        t.run("""
        cd ~/work/worklog
        code .
        """)

    def create(self):
        t.run("""
        cd ~/Documents
        nohup screenkey -t 1 &
        ./UnityHub.AppImage
        """)

    def sleep(self):
        self._kill()

    def play(self):
        self._go_to("~/CS/notebooks")
        self._kill()
        t.run("""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate cling

nohup jupyter-lab ~/CS/notebooks &
google-chrome "https://leetcode.com/problemset/all/"
                """, wait=False)

    def lab(self):
        self._go_to("~/CS/notebooks")
        self._kill()
        t.run("""
nohup jupyter-lab ~/CS/notebooks &
google-chrome "https://keras.io/examples/" &
        """, wait=False)

    def ui(self):
        path = "~/CS/freedom/2021"
        self._go_to(path)

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
        self._go_to(path)
        self._kill()
        t.run_command(f"""
        google-chrome "https://google.com" &
        #terminator --working-directory="{path}"
        cd {path}
        nohup pycharm-community &
        nohup xournalpp "~/CS/auto_everything/plans.xopp" &
        """)

    def cpp(self):
        path = "~/CS/auto_everything"
        self._go_to(path)
        self._kill()
        t.run_command(f"""
        google-chrome "https://google.com" &
        cd {path}
        nohup pycharm-community &
        nohup clion &
        nohup xournalpp "~/CS/auto_everything/plans.xopp" &
        """)

    def math(self):
        path = "/home/yingshaoxo/Documents/HighLevelMathVideos"
        self._go_to(path)
        controller.write("xdg-open .")
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

    def en(self):
        self._kill()
        t.run(f"""
google-chrome "https://translate.google.com/" &

xdg-open "/home/yingshaoxo/Downloads/SYNC/Resources/Books/English/2010-2020考研英语一答案（一键打印版）.pdf"

nohup xournalpp "/home/yingshaoxo/Downloads/SYNC/Resources/Books/English/2010-2020考研英语一真题合集（一键打印）.pdf.xopp" &
        """)

        t.run("""
        xdg-open ~/Videos/doing &
        #terminator --working-directory="~/Videos" &
        obs-studio
        """, wait=False)

    def record(self):
        path = "~/Videos"
        self._go_to(path)
        self._kill()
        t.run("""
        xdg-open ~/Videos/doing &
        #terminator --working-directory="~/Videos" &
        nohup obs-studio &
        firefox
        """, wait=False)

    def draw(self):
        path = "/home/yingshaoxo/Downloads/SYNC/Personal/Art"
        self._go_to(path)
        self._kill()
        t.run(f"""
        google-chrome "https://inkscape.org/doc/keys.html" &
        xdg-open {path} &
        inkscape
        """, wait=False)

    def pi(self):
        t.run("""
terminator -e "ssh pi@192.168.49.17"
        """)

    def server(self, num=""):
        if num == "":
            t.run("""
    terminator -e "ssh root@149.28.229.110"
            """)
        else:
            t.run(f"""
    Copy server_password {num}
    terminator -e "ssh ubuntu@192.168.101.{num}"
            """)

    def android(self):
        t.run("""
cd ~/Android/Sdk/emulator/
./emulator @Pixel_3a_API_30_x86 -no-snapshot-load
        """)


py.fire(Mission)
py.make_it_global_runnable(executable_name="Start")
