#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Terminal, Python
from auto_everything.video import Video

t = Terminal()
py = Python()
video = Video()

import os

class Tools():
    def link(self):
        files = []
        for file in os.listdir('doing'):
            files.append(os.path.abspath(os.path.join('doing', file)))
        files.sort(key=os.path.getmtime)
        video.link_videos(files, os.path.abspath('./doing.mp4'))

    def nosilence(self, db=30, interval=0.5):
        source = os.path.abspath('./doing.mp4')
        target = os.path.abspath('./nosilence.mp4')
        video.remove_silence_parts_from_video(source, target, db, interval)

    def speedupsilence(self, db=30, speed=20):
        source = os.path.abspath('./doing.mp4')
        target = os.path.abspath('./speedupsilence.mp4')
        video.speedup_silence_parts_in_video(source, target, db, speed)

py.make_it_runnable()
py.fire(Tools)
