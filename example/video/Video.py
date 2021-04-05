#!/usr/bin/env /usr/bin/python3
import os
from auto_everything.base import Terminal, Python
from auto_everything.video import Video, DeepVideo

os.chdir("/home/yingshaoxo/Videos")

t = Terminal()
py = Python()
video = Video()
deepVideo = DeepVideo()


class Tools():
    def link(self):
        files = []
        for file in os.listdir('doing'):
            files.append(os.path.abspath(os.path.join('doing', file)))
        files.sort(key=os.path.getmtime)
        video.link_videos(files, os.path.abspath('./doing.mp4'), method=2)

    def preprocessing(self):
        if len(os.listdir("doing")) == 1:
            t.run_command("rm doing.mp4")
            t.run_command("mv doing/*.mkv doing.mp4")
        elif len(os.listdir("doing")) > 1:
            self.link()

    def nosilence(self, db=19, interval=0.4, skip_noise=0):  # 21, 0.7
        self.preprocessing()
        source = os.path.abspath('./doing.mp4')
        if not os.path.exists(source):
            self.link()
        target = os.path.abspath('./nosilence.mp4')
        video.remove_silence_parts_from_video(source, target, db, interval, skip_sharp_noise=bool(skip_noise))
        #deepVideo.remove_silence_parts_from_video(source, target, 0.7)

    def speedupsilence(self, db=20, speed=20):  # 21 5
        self.preprocessing()
        source = os.path.abspath('./doing.mp4')
        if not os.path.exists(source):
            self.link()
        target = os.path.abspath('./speedupsilence.mp4')
        video.speedup_silence_parts_in_video(source, target, db, speed)

    def removeTopAD(self):
        source = os.path.abspath('./nosilence.mp4')
        target = os.path.abspath('./cropped.mp4')
        video.removeTopAndBottomOfAVideo(source, target)

    def splits(self, parts):
        source = os.path.abspath('./nosilence.mp4')
        target = os.path.abspath('./outputs')
        video.splitVideoToParts(source, target, parts)

    def hi(self):
        print("\n\nHi! I'm yingshaoxo!")
        print("\nThis is my channel: https://www.youtube.com/channel/UCbT9GDmkqf555ATReJor6ag")
        print("\n\n")

    def add(self):
        source = os.path.abspath('./doing.mp4')
        target = os.path.abspath('./target.mp4')
        t.run(f"""
        ffmpeg -y -i "{source}" -vf subtitles=captions.srt "{target}"
                """)

    def make(self, db=30, minimum_interval=1.4):
        source = os.path.abspath('./doing.mp4')
        target = os.path.abspath('./nosilence.mp4')
        video.humanly_remove_silence_parts_from_video(source_video_path=source, target_video_path=target, db_for_split_silence_and_voice=db, minimum_interval=minimum_interval)


py.fire(Tools)
py.make_it_global_runnable(executable_name="Video")
