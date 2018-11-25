#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
from auto_everything.video import Video
py = Python()
t = Terminal()

video = Video()

import os
import time

class Tools():
    def copy(self, file_path):
        """
        copy a file to another disk
        """
        file_path = os.path.abspath(file_path)
        t.run(f"""
sudo mkdir /media/newhd
sudo umount /dev/sda5
sudo mount /dev/sda5 /media/newhd
        """)
        t.run(f"""
cp '{file_path}' '/media/newhd/My Classroom' -fr
        """)

    def combine(self):
        video.combine_all_mp4_in_a_folder("/home/yingshaoxo/Videos/doing")

    def nosilence(self, db):
        video = Video("/home/yingshaoxo/Videos/doing.mp4")
        video.humanly_remove_silence_parts_from_video(db_for_split_silence_and_voice=db, remove_noise=True)

    def demo(self, db=None):
        video = Video("/home/yingshaoxo/Videos/doing.mp4")
        if db == None:
            t.run("rm demo.mp4")
            t.run("""ffmpeg -i './doing.mp4' -ss 0 -t 60 demo.mp4""")
        else:
            t.run("rm new_demo.mp4")
            video = Video("/home/yingshaoxo/Videos/demo.mp4")
            video.humanly_remove_silence_parts_from_video(db_for_split_silence_and_voice=db)
    def test(self):
        video = Video("/home/yingshaoxo/Videos/demo.mp4")
        video.humanly_remove_silence_parts_from_video(db_for_split_silence_and_voice=25, remove_noise=True)
        #video = Video("/home/yingshaoxo/Videos/new_doing.mp4")
        #video.remove_noise_from_video()


py.make_it_runnable()
py.fire(Tools)
