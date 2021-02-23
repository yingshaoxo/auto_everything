#!/usr/bin/env /usr/bin/python3
import os
from auto_everything.base import Terminal, Python
from auto_everything.video import Video

t = Terminal()
py = Python()
video = Video()


class Tools():
    def link(self):
        files = []
        for file in os.listdir('doing'):
            files.append(os.path.abspath(os.path.join('doing', file)))
        files.sort(key=os.path.getmtime)
        video.link_videos(files, os.path.abspath('./doing.mp4'))

    def nosilence(self, db=21, interval=0.7):
        source = os.path.abspath('./doing.mp4')
        if not os.path.exists(source):
            self.link()
        target = os.path.abspath('./nosilence.mp4')
        video.remove_silence_parts_from_video(source, target, db, interval)

    def speedupsilence(self, db=21, speed=5):
        source = os.path.abspath('./doing.mp4')
        target = os.path.abspath('./speedupsilence.mp4')
        video.speedup_silence_parts_in_video(source, target, db, speed)

    def removeTopAD(self):
        source = os.path.abspath('./nosilence.mp4')
        target = os.path.abspath('./cropped.mp4')
        video.removeTopAndBottomOfAVideo(source, target)

    def splits(self, parts):
        source = os.path.abspath('./cropped.mp4')
        target = os.path.abspath('./outputs')
        video.splitVideoToParts(source, target, 3)


py.make_it_runnable()
py.fire(Tools)
