#!/usr/bin/env /Users/yingshaoxo/Library/Caches/pypoetry/virtualenvs/auto-everything-_Gc1gPdN-py3.10/bin/python
import inquirer
import os
from auto_everything.base import Terminal, Python
from auto_everything.video import Video, DeepVideo
from auto_everything.disk import Disk


t = Terminal()
py = Python()
video = Video()
deepVideo = DeepVideo()
disk = Disk()

t.debug = True


RootDIR = "/Users/yingshaoxo/Movies/Videos"


class Tools:
    def __init__(self):
        os.chdir(RootDIR)

    def run(self):
        questions = [
            inquirer.List(
                "function",
                message="What is the function you want to call?",
                choices=["nosilence", "speedupsilence"],
            ),
            # inquirer.Text('db', message="What's db that split the voice and silence")
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            print("You must choose.")
            return

        function = answers.get("function")
        if function == "nosilence":
            questions = [
                inquirer.Text(
                    "db",
                    message="What's db that split the voice and silence? (default to 50)",
                ),
                inquirer.Text(
                    "interval",
                    message="What's minimum interval that when small than that, we never treat it as silence? (default to 1.7)",
                ),
            ]
            answers = inquirer.prompt(questions)
            if answers is None:
                print("You must choose.")
                return

            db = answers.get("db")
            interval = answers.get("interval")

            if db is None or db.strip() == "":
                db = 50
            if interval is None or interval.strip() == "":
                interval = 1.7

            db = int(db.strip())  # type: ignore
            interval = float(interval.strip())  # type: ignore

            self.nosilence(db=db, interval=interval)
        elif function == "speedupsilence":
            questions = [
                inquirer.Text(
                    "db",
                    message="What's db that split the voice and silence? (default to 35)",
                ),
                inquirer.Text(
                    "speed",
                    message="What's video speed that you want for silence part? (default to 50)",
                ),
            ]
            answers = inquirer.prompt(questions)
            if answers is None:
                print("You must choose.")
                return

            db = answers.get("db")
            speed = answers.get("speed")

            if db is None or db.strip() == "":
                db = 35
            if speed is None or speed.strip() == "":
                speed = 50

            db = int(db.strip())  # type: ignore
            speed = int(speed.strip())  # type: ignore

            self.speedupsilence(db=db, speed=speed)

    def link(self):
        files = []
        for file in os.listdir(t.fix_path("./doing")):
            splits = file.split(".")
            if len(splits) > 0:
                if splits[1] in ["mp4", "mkv"]:
                    files.append(os.path.abspath(os.path.join("doing", file)))
        files.sort(key=os.path.getmtime)
        video.link_videos(files, os.path.abspath("./doing.mp4"), method=2)

    def preprocessing(self):
        if not disk.exists("./doing"):
            return

        files = disk.get_files("doing", recursive=False, type_limiter=[".mp4", ".mkv"])
        files = [file for file in files if file != ".DS_Store"]
        if len(files) == 1:
            t.run_command(
                t.fix_path(
                    f"""
                cd {RootDIR}
                rm -fr doing.mp4
                mv doing/*.* doing.mp4
                    """
                )
            )
        elif len(files) > 1:
            self.link()

    def nosilence(self, db=19, interval=0.4, skip_noise=0):  # 21, 0.7
        self.preprocessing()
        source = os.path.abspath("./doing.mp4")
        if not disk.exists(source):
            files = disk.get_files(".", recursive=False, type_limiter=[".mp4", ".mkv"])

            questions = [
                inquirer.List(
                    "file",
                    message="What file you want to process?",
                    choices=files,
                ),
            ]
            answers = inquirer.prompt(questions)
            if answers is None:
                print("You must choose.")
                return

            source = answers.get("file")
            if source is None:
                exit()
        print(source)
        target = os.path.abspath("./nosilence.mp4")
        video.remove_silence_parts_from_video(
            source, target, db, interval, skip_sharp_noise=bool(skip_noise)
        )
        # deepVideo.remove_silence_parts_from_video(source, target, 0.7)

    def speedupsilence(self, db=35, speed=30):  # 21 5
        self.preprocessing()
        source = os.path.abspath("./doing.mp4")
        if not disk.exists(source):
            source = os.path.abspath(".")
        target = os.path.abspath("./speedupsilence.mp4")
        video.speedup_silence_parts_in_video(source, target, db, speed)

    def addmusic(self, song):
        video.add_background_music_files_into_video(
            source_file_path="./speedupsilence.mp4",
            target_file_path="output.mp4",
            musicFiles=[
                # "/Users/yingshaoxo/Downloads/永远都会在 - 旅行团乐队.mp3",
                # "/Users/yingshaoxo/Downloads/wish you were gay - Billie Eilish.mp3"
                song
            ],
            preDecreaseDBValueForTheMusic=18,
            howManyDBYouWannaTheMusicToDecreaseWhenYouSpeak=15,
        )

    def removeTopAD(self):
        source = os.path.abspath("./nosilence.mp4")
        target = os.path.abspath("./cropped.mp4")
        video.removeTopAndBottomOfAVideo(source, target)

    def splits(self, parts):
        source = os.path.abspath("./nosilence.mp4")
        target = os.path.abspath("./outputs")
        video.splitVideoToParts(source, target, parts)

    def hi(self):
        print("\n\nHi! I'm yingshaoxo!")
        print(
            "\nThis is my channel: https://www.youtube.com/channel/UCbT9GDmkqf555ATReJor6ag"
        )
        print("\n\n")

    def add(self):
        source = os.path.abspath("./doing.mp4")
        target = os.path.abspath("./target.mp4")
        t.run(
            f"""
        ffmpeg -y -i "{source}" -vf subtitles=captions.srt "{target}"
                """
        )

    def make(self):
        self.preprocessing()

        db = 21
        minimum_interval = 1.7
        skip = 1

        source = os.path.abspath("./doing.mp4")
        target = os.path.abspath("./nosilence.mp4")
        video.remove_silence_parts_from_video(
            source, target, db, minimum_interval, skip_sharp_noise=skip == 1
        )

    def compress(self, folder):
        os.chdir(t.run_command("pwd"))

        path = os.path.abspath(folder)
        video.compress_videos_in_a_folder(path)

    def fix(self, folder):
        os.chdir(t.run_command("pwd"))

        path = os.path.abspath(folder)
        video.fix_corrupt_videos_in_a_folder(path)


py.fire(Tools)
py.make_it_global_runnable(executable_name="Video")
