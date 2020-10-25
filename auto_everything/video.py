import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, concatenate_videoclips
import shutil
import datetime
import librosa
import numpy as np
import os
import math
import multiprocessing
import json

import pyaudio
import sys
import wave
import subprocess

from typing import List, Tuple
from auto_everything.base import Terminal, Python, IO
from auto_everything.network import Network
from auto_everything.disk import Disk
t = Terminal(debug=True)
py = Python()
io_ = IO()
network = Network()
disk = Disk()


def print_split_line():
    print('\n' + '-'*20 + '\n')


def done():
    print_split_line()
    print('We are done, sir.')
    print_split_line()


def get_directory_name(path):
    return os.path.dirname(path)


def add_path(path1, path2):
    return os.path.join(path1, path2)


def try_to_get_absolutely_path(path):
    abs_path = os.path.abspath(path)
    if os.path.isabs(abs_path) or os.path.exists(abs_path):
        return abs_path
    else:
        return path


def make_sure_source_is_absolute_path(path):
    path_list = []
    if isinstance(path, str):
        path_list.append(path)
    else:
        path_list = path

    for p in path_list:
        if os.path.isabs(p):
            pass
        else:
            print("for source file: you must give me absolute path")
            exit()


def make_sure_target_is_absolute_path(path):
    path_list = []
    if isinstance(path, str):
        path_list.append(path)
    else:
        path_list = path

    for p in path_list:
        p = get_directory_name(p)
        if os.path.isabs(p):
            pass
        else:
            print("for target file: you must give me absolute path")
            exit()


def make_sure_target_does_not_exist(path):
    path_list = []
    if isinstance(path, str):
        path_list.append(path)
    else:
        path_list = path

    for p in path_list:
        if os.path.exists(p):
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                r = os.remove(p)
                if r is False:
                    print(
                        f"I can't remove target '{p}' for you, please check your permission")
                    exit()


def convert_video_to_wav(source_video_path, target_wav_path):
    source_video_path = try_to_get_absolutely_path(source_video_path)
    make_sure_source_is_absolute_path(source_video_path)
    target_wav_path = try_to_get_absolutely_path(target_wav_path)
    make_sure_target_is_absolute_path(target_wav_path)

    make_sure_target_does_not_exist(target_wav_path)

    t.run(f"""
        ffmpeg -i "{source_video_path}" "{target_wav_path}"
    """)

    return target_wav_path


def get_wav_infomation(wav_path):
    wav_path = try_to_get_absolutely_path(wav_path)
    make_sure_source_is_absolute_path(wav_path)

    y, sr = librosa.load(wav_path, sr=None)
    return y, sr


# we'll use ffmpeg to do the real work
class Video():
    """
    This is a powerful video module

    It's based on:
    1. ubuntu core
    2. librosa
    3. ffmpeg
    4. moviepy
    """

    def __init__(self):
        self._cpu_core_numbers = multiprocessing.cpu_count()

    def _get_voice_parts(self, source_audio_path, top_db, minimum_interval_time_in_seconds=1.0):
        y, sr = get_wav_infomation(source_audio_path)
        minimum_interval_samples = librosa.core.time_to_samples(
            minimum_interval_time_in_seconds, sr)

        def ignore_short_noise(parts):
            # ignore short noise
            new_parts = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = (part[0] - parts[index-1][1])
                    if (noise_interval > minimum_interval_samples):
                        time_gaps = (part[0]-parts[index-1][1])*0.1
                        # we fear if the time_gaps is too long
                        if time_gaps >= minimum_interval_samples:
                            time_gaps = minimum_interval_samples // 2
                        new_parts.append(
                            [parts[index-1][1],
                             parts[index-1][1] + time_gaps
                             ]
                        )
                        new_parts.append(
                            [part[0] - time_gaps,
                             part[0]
                             ]
                        )
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index-1][1], part[0]])
                        new_parts.append(list(part))

            the_missing_final = new_parts[-1][1]
            # combine continuous voice
            final_parts = []
            first = -1
            for index, part in enumerate(new_parts):
                if index == 0:
                    final_parts.append(part)
                    continue
                else:
                    inverval = (part[0] - new_parts[index-1][1])
                    if (inverval == 0):
                        if first == -1:
                            first = new_parts[index-1][0]
                    else:
                        if (first == -1):
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append([first, new_parts[index-1][1]])
                            first = -1

            final_parts.append([final_parts[-1][1], the_missing_final])

            return np.array(final_parts)

        parts = librosa.effects.split(y, top_db=top_db)  # return samples
        parts = ignore_short_noise(parts)

        # new_y = librosa.effects.remix(self._y, parts) # receive samples
        # target_file_path = os.path.join(self._video_directory, "new_" + self._audio_name)
        # if t.exists(target_file_path):
        #    os.remove(target_file_path)
        # librosa.output.write_wav(target_file_path, new_y, self._sr)

        def from_samples_to_seconds(parts):
            parts = librosa.core.samples_to_time(parts, sr)  # return seconds
            new_parts = []

            def seconds_to_string_format(num):
                return str(datetime.timedelta(seconds=num))
            for part in parts:
                part1 = seconds_to_string_format(part[0])
                part2 = seconds_to_string_format(part[1])
                new_parts.append([part1, part2])
            return new_parts

        parts[0] = [0, parts[0][1]]
        parts = from_samples_to_seconds(parts)

        return parts[1:]

    def _get_voice_and_silence_parts(self, source_audio_path, top_db, minimum_interval_time_in_seconds=1.5):
        # let's assume 1=voice, 0=noise
        y, sr = get_wav_infomation(source_audio_path)
        minimum_interval_samples = librosa.core.time_to_samples(
            minimum_interval_time_in_seconds, sr)

        parts = librosa.effects.split(y, top_db=top_db)  # return samples

        def ignore_short_noise(parts):
            # ignore short noise
            new_parts = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = (part[0] - parts[index-1][1])
                    if (noise_interval > minimum_interval_samples):
                        new_parts.append(
                            [parts[index-1][1], parts[index-1][1]])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index-1][1], part[0]])
                        new_parts.append(list(part))

            the_missing_final = new_parts[-1][1]
            # combine continuous voice
            final_parts = []
            first = -1
            for index, part in enumerate(new_parts):
                if index == 0:
                    final_parts.append(part)
                    continue
                else:
                    inverval = (part[0] - new_parts[index-1][1])
                    if (inverval == 0):
                        if first == -1:
                            first = new_parts[index-1][0]
                    else:
                        if (first == -1):
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append([first, new_parts[index-1][1]])
                            first = -1

            final_parts.append([final_parts[-1][1], the_missing_final])

            return np.array(final_parts)

        parts = ignore_short_noise(parts)
        parts = parts[1:]

        def from_samples_to_seconds(part):
            part = librosa.core.samples_to_time(part, sr)  # return seconds

            def seconds_to_string_format(num):
                return str(datetime.timedelta(seconds=num))
            return [seconds_to_string_format(part[0]), seconds_to_string_format(part[1])]

        voice_and_silence_parts = []
        for index, part in enumerate(parts):
            first = part[0]
            second = part[1]
            if index == 0:
                if first != 0:
                    voice_and_silence_parts.append(
                        [0, from_samples_to_seconds([0, first])])
                    voice_and_silence_parts.append(
                        [1, from_samples_to_seconds([first, second])])
            else:
                voice_and_silence_parts.append(
                    [0, from_samples_to_seconds([parts[index-1][1], first])])
                voice_and_silence_parts.append(
                    [1, from_samples_to_seconds([first, second])])

        def remove_unwanted_parts(voice_and_silence_parts):
            return [part for part in voice_and_silence_parts if part[1][0] != part[1][1]]

        voice_and_silence_parts = remove_unwanted_parts(
            voice_and_silence_parts)
        return voice_and_silence_parts

    def _evaluate_voice_parts(self, parts):
        from dateutil.parser import parse
        new_parts = []
        start_timestamp = 0
        for part in parts:
            part1 = parse(part[0]).timestamp()
            part2 = parse(part[1]).timestamp()
            if (start_timestamp == 0):
                start_timestamp = part1
            new_parts.append(
                [part1 - start_timestamp, part2 - start_timestamp])

        all_silence = 0
        for index, part in enumerate(new_parts):
            if index == 0:
                continue
            all_silence += (part[0] - new_parts[index-1][1])

        ratio = all_silence/new_parts[-1][1]
        return ratio

    def split_video_by_time_part(self, source_video_path, target_video_path, part):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        try:
            time_start = part[0]
            time_end = part[1]
        except Exception as e:
            print(e)
            print(part)
            print("time part is a list: [time_start, time_end]")
            exit()

        t.run(f"""
            ffmpeg -i "{source_video_path}" -ss {time_start} -to {time_end} -threads 8 "{target_video_path}"
        """)

        done()

    def _split_video_to_parts_by_time_intervals(self, source_video_path, target_folder, time_intervals):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_folder)

        make_sure_target_does_not_exist(target_folder)
        if not t.exists(target_folder):
            os.mkdir(target_folder)

        for index, part in enumerate(time_intervals):
            index = (6-len(str(index)))*'0' + str(index)

            target_video_path = add_path(target_folder, str(index)+".mp4")

            self.split_video_by_time_part(
                source_video_path, target_video_path, part)

        done()

    def link_videos(self, source_video_path_list, target_video_path, method=2, preset="ultrafast"):
        """
        concatenate videos one by one

        Parameters
        ----------
        source_video_path_list: list of video path
            those videos you want to concatenate

        target_video_path: string
            where to save the concatenated video

        method: int
            1 to use ffmpeg(low quality), 2 to use moviepy(high quality)
        """
        source_video_path_list = [try_to_get_absolutely_path(
            f) for f in source_video_path_list]
        make_sure_source_is_absolute_path(source_video_path_list)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_target_is_absolute_path(target_video_path)

        if method == 1:
            working_dir = get_directory_name(target_video_path)
            txt_file_path = add_path(working_dir, 'temp_list.txt')
            text = ''
            for file_path in source_video_path_list:
                text += "file " + f"'{file_path}'" + '\n'
            io_.write(txt_file_path, text)

            make_sure_target_does_not_exist(target_video_path)

            combine_command = f"ffmpeg -f concat -safe 0 -i '{txt_file_path}' '{target_video_path}'"
            t.run(combine_command, wait=True)

            make_sure_target_does_not_exist(txt_file_path)
        elif method == 2:
            # for the stupid moviepy library, it will case memory leak if you give it too much videos
            print(source_video_path_list)
            clip_list = [VideoFileClip(clip)
                         for clip in source_video_path_list]
            final_clip = concatenate_videoclips(clip_list)
            final_clip.write_videofile(
                target_video_path, threads=self._cpu_core_numbers, preset=preset)

            for clip in clip_list:
                clip.close()
                del clip

            del final_clip

        done()

    def combine_all_mp4_in_a_folder(self, source_folder, target_video_path, sort_by_time=True, method=1):
        """
        concatenate all videos in a folder

        Parameters
        ----------
        sort_by_time: bool
            when true, we sort by time
            when false, we sort by name(1, 2, 3)

        method: int
            1 to use ffmpeg(low quality), 2 to use moviepy(high quality)
        """
        filelist = [os.path.join(source_folder, f) for f in os.listdir(
            source_folder) if f.endswith(".mp4")]

        if (sort_by_time is False):
            filelist = list(sorted(filelist))
        else:
            filelist.sort(key=lambda x: os.path.getmtime(x))

        self.link_videos(source_video_path_list=filelist,
                         target_video_path=target_video_path, method=method)

        if sort_by_time is False:
            make_sure_target_does_not_exist(source_folder)

        done()

    def remove_noise_from_video(self, source_video_path, target_video_path, degree=0.21, noise_capture_length=None):
        """
        Just as said, remove noise from video
        """
        degree = str(degree)

        source_video_path = try_to_get_absolutely_path(source_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_target_is_absolute_path(target_video_path)

        if not noise_capture_length:
            noise_capture_length = "1"
        else:
            noise_capture_length = str(noise_capture_length)

        working_dir = get_directory_name(target_video_path)

        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, 'audio_for_remove_noise_from_video.wav'))
        noise_sample_wav_path = add_path(working_dir, 'noise_sample_wav.wav')
        noise_prof_path = add_path(working_dir, 'noise_prof.prof')
        no_noise_wav_path = add_path(working_dir, "no_noise_wav.wav")
        loudnorm_wav_path = add_path(working_dir, "loudnorm_wav.wav")

        make_sure_target_does_not_exist(target_video_path)
        make_sure_target_does_not_exist(
            [noise_sample_wav_path, noise_prof_path, no_noise_wav_path, loudnorm_wav_path])

        t.run(f"""
            ffmpeg -i "{source_video_path}" -acodec pcm_s16le -ar 128k -vn -ss 00:00:00.0 -t 00:00:0{noise_capture_length}.0 "{noise_sample_wav_path}"
        """)

        t.run(f"""
            sox "{noise_sample_wav_path}" -n noiseprof "{noise_prof_path}"
        """)

        t.run(f"""
            sox "{audio_path}" "{no_noise_wav_path}" noisered "{noise_prof_path}" {degree}
        """)

        t.run(f"""
            ffmpeg -i "{no_noise_wav_path}" -af loudnorm=I=-23:LRA=1 -ar 48000 "{loudnorm_wav_path}"
        """)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -i "{loudnorm_wav_path}" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k "{target_video_path}"
        """)

        make_sure_target_does_not_exist(
            [audio_path, noise_sample_wav_path, noise_prof_path, no_noise_wav_path, loudnorm_wav_path])

        done()

    def remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice, minimum_interval_time_in_seconds=None, voice_only=False):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`, but for some case if the volume is too small, `30` would be fine
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        voice_only: bool
            if true, it only returns the path of silence removed mp3 file
        """

        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, disk.get_hash_of_a_path(source_video_path)+'audio_for_remove_silence_parts_from_video.wav'))
        temp_video_path = add_path(
            working_dir, disk.get_hash_of_a_path(source_video_path)+'temp_for_remove_silence_parts_from_video.mp4')

        if minimum_interval_time_in_seconds is None:
            parts = self._get_voice_parts(audio_path, top_db)
        else:
            parts = self._get_voice_parts(
                audio_path, top_db, minimum_interval_time_in_seconds)

        # """
        parent_clip = VideoFileClip(source_video_path)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            try:
                time_duration = (datetime.datetime.strptime(
                    part[1], '%H:%M:%S.%f') - datetime.datetime.strptime(part[0], '%H:%M:%S.%f')).seconds
                print(str(int(index/length*100))+"%,", "-".join(
                    [p.split(".")[0] for p in part]) + ",", "cut " + str(time_duration) + " seconds")
            except Exception as e:
                print(e)
            clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)

        if not voice_only:
            concat_clip.write_videofile(
                target_video_path, threads=self._cpu_core_numbers)
            concat_clip.close()
            del concat_clip
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
        else:
            if len(target_video_path.split(".")) >= 2:
                target_audio_path = ".".join(
                    target_video_path.split(".")[:-1]) + ".mp3"
            else:
                target_audio_path = target_video_path + ".mp3"
            make_sure_target_does_not_exist(target_audio_path)
            concat_clip.audio.write_audiofile(target_audio_path, fps=44100)
            concat_clip.close()
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
            return target_audio_path

        done()

    def humanly_remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice, minimum_interval=1):
        """
        No difference with the last one, but in this function, you can check how many silence you can get rid of.
        Then you make the decision wheather you want to do this or not

        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        """
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        source_video_path = os.path.abspath(source_video_path)
        target_video_path = os.path.abspath(target_video_path)

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, 'audio_for_humanly_remove_silence_parts_from_video.wav'))

        temp_video_path = add_path(
            working_dir, 'temp_for_humanly_remove_silence_parts_from_video.mp4')

        try:
            # parts = self._get_voice_parts(
            #    source_audio_path=audio_path, top_db=db_for_split_silence_and_voice)
            # ratio = int(self._evaluate_voice_parts(parts) * 100)
            target_audio_path = self.remove_silence_parts_from_video(
                source_video_path, target_video_path, db_for_split_silence_and_voice=db_for_split_silence_and_voice, minimum_interval_time_in_seconds=minimum_interval, voice_only=True)
        except Exception as e:
            print(e)
            print()
            print(
                "You probably gave me a wroung db value, try to make it smaller and try it again")
            exit()

        make_sure_target_does_not_exist(temp_video_path)
        make_sure_target_does_not_exist(audio_path)

        answer = input(
            f"Are you happy with the audio file: {target_audio_path}% ? (y/n) (you may have to exit this script to hear your audio from your computers)")
        if answer.strip() == "y":
            print("ok, let's do it!")

            make_sure_target_does_not_exist(target_audio_path)
            self.remove_silence_parts_from_video(
                source_video_path, target_video_path, db_for_split_silence_and_voice=db_for_split_silence_and_voice, minimum_interval_time_in_seconds=minimum_interval)

            done()
        else:
            print()
            print("you may want to change the db, and try again.")
            exit()

    def speedup_video(self, source_video_path, target_video_path, speed=1.5):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        speed: float
            how quick you want the video to be
        """
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        speed = float(speed)
        video_speed = str(float(1/speed))[:6]

        if speed <= 4:
            parts = math.ceil(speed/2)
            value_of_each_part = str(speed ** (1/parts))[:6]
            audio_speed = ",".join(
                [f"atempo={value_of_each_part}" for i in range(parts)])

            t.run(f"""
                ffmpeg -i "{source_video_path}" -filter_complex "[0:v]setpts={video_speed}*PTS[v];[0:a]{audio_speed}[a]" -map "[v]" -map "[a]" "{target_video_path}"
            """)

            done()
        else:
            self._speedup_video_with_moviepy(
                source_video_path, target_video_path, speed=speed)

    def _speedup_video_with_moviepy(self, source_video_path, target_video_path, speed=4):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        clip = VideoFileClip(source_video_path).without_audio().fx(
            vfx.speedx, speed)
        clip.write_videofile(target_video_path, threads=self._cpu_core_numbers)

        done()

    def speedup_silence_parts_in_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice, speed=4):
        """
        Instead remove silence, we can speed up the silence parts in a video

        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`
        speed: float
            how quick you want the silence parts to be
        """
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, disk.get_hash_of_a_path(source_video_path)+'audio_for_speedup_silence_parts_in_video.wav'))

        voice_and_silence_parts = self._get_voice_and_silence_parts(
            audio_path, top_db)

        make_sure_target_does_not_exist(audio_path)
        parent_clip = VideoFileClip(source_video_path)
        clip_list = []
        length = len(voice_and_silence_parts)
        for index, part in enumerate(voice_and_silence_parts):
            if len(part[1][0].split(".")) < 2:
                part[1][0] += ".000000"
            try:
                time_duration = (datetime.datetime.strptime(
                    part[1][1], '%H:%M:%S.%f') - datetime.datetime.strptime(part[1][0], '%H:%M:%S.%f')).seconds
                print(str(int(index/length*100))+"%,", "-".join([p.split(".")[
                      0] for p in part[1]]) + ",", "cut " + str(time_duration) + " seconds")
            except Exception as e:
                print(e)
            if part[0] == 1:  # voice
                clip_list.append(parent_clip.subclip(part[1][0], part[1][1]))
            else:  # silence
                clip_list.append(
                    parent_clip.subclip(part[1][0], part[1][1]).without_audio().fx(
                        vfx.speedx, speed
                    )
                )

        concat_clip = concatenate_videoclips(clip_list)

        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers)
        concat_clip.close()
        del concat_clip

        done()

    def replace_video_with_a_picture(self, source_video_path, target_video_path, picture):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        picture: string
            the path of that picture
        """
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        picture = try_to_get_absolutely_path(picture)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_is_absolute_path(picture)
        make_sure_target_does_not_exist(target_video_path)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -i "{picture}" -filter_complex "[1][0]scale2ref[i][v];[v][i]overlay" -c:a copy "{target_video_path}"
        """)

        done()

    def get_mp3_from_video(self, source_video_path, target_video_path):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        delay = float(delay)
        delay = str(delay)

        t.run(f"""
            ffmpeg -i "{source_video_path}" "{source_video_path}"
        """)

        done()

    def delay_audio_in_video(self, source_video_path, target_video_path, delay):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        delay = float(delay)
        delay = str(delay)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -itsoffset {delay} -i "{source_video_path}" -map 0:v -map 1:a -c copy "{target_video_path}"
        """)

        done()

    def increase_audio_volume_in_video(self, source_video_path, target_video_path, times):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        times: float
            2 times the source_video volume or 3 times the source_video volume
        """
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        times = float(times)
        times = str(times)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -vcodec copy -af "volume={times}dB" "{target_video_path}"
        """)

        done()

    def compress_videos_in_a_folder(self, source_folder, fps: int = 29, resolution: Tuple[int, int] = None, preset: str = 'placebo'):
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(working_dir, 'compressed_' +
                              os.path.basename(source_folder))
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        filelist = [os.path.join(source_folder, f) for f in os.listdir(
            source_folder) if f.endswith(".mp4")]

        def convert_bytes(num):
            """
            this function will convert bytes to MB.... GB... etc
            """
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if num < 1024.0:
                    return (int(float(f'{num:.1f}')), f'{x}')
                num /= 1024.0

            return (0, 0)

        for file in filelist:
            basename = os.path.basename(file)
            target_video_path = add_path(new_folder, basename)
            make_sure_target_does_not_exist(target_video_path)

            #size, unit = convert_bytes(os.path.getsize(file))
            # if unit == "GB":
            #    if size > 2:
            if fps and resolution and preset:
                t.run(f"""
                    ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale={resolution[0]}:{resolution[1]} -r {fps} -preset {preset} "{target_video_path}"
                """)
            else:
                t.run(f"""
                    ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale=-2:720 "{target_video_path}"
                """)

        done()

    def format_videos_in_a_folder(self, source_folder):
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(working_dir, 'formated_' +
                              os.path.basename(source_folder))
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        filelist = [os.path.join(source_folder, f) for f in os.listdir(
            source_folder) if f.endswith(".mp4")]

        for file in filelist:
            basename = os.path.basename(file)
            target_video_path = add_path(new_folder, basename)
            make_sure_target_does_not_exist(target_video_path)

            t.run(f"""
                ffmpeg -i "{file}" -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 "{target_video_path}"
            """)

        done()


class DeepVideo():
    """
    For this one, I'll use deep learning.

    It's based on:
    1. ubuntu core
    2. vosk
    3. ffmpeg
    4. moviepy
    """

    def __init__(self):
        from pathlib import Path

        self._cpu_core_numbers = multiprocessing.cpu_count()

        self.config_folder = Path(
            "~/.auto_everything").expanduser() / Path("video")
        if not os.path.exists(self.config_folder):
            t.run_command(f"mkdir -p {self.config_folder}")

        # download
        zip_file = self.config_folder / Path("vosk-en.zip")
        if not disk.exists(zip_file):
            success = network.download(
                "http://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.3.zip", zip_file, "30MB")
            if success:
                print("download successfully")
            else:
                print("download error")

        # uncompress
        self.vosk_model_folder = self.config_folder/Path("model")
        if not self.vosk_model_folder.exists():
            disk.uncompress(zip_file, self.vosk_model_folder)

    def __time_interval_filter(self, data, minimum_interval_time_in_seconds: float = 0.0, video_length: float = None):
        temp_data = []
        length = len(data)
        for index, item in enumerate(data):
            start = item['start']
            end = item['end']
            start = start - minimum_interval_time_in_seconds
            end = end + minimum_interval_time_in_seconds
            if index == 0:
                start = item['start'] - minimum_interval_time_in_seconds
                if start < 0:
                    start = 0.0
            if index == length-1:
                end = item['end']
            temp_data.append([start, end])
        parts = []
        index = 0
        length = len(temp_data)
        if length >= 2:
            while index <= length-1:
                first_start = temp_data[index][0]
                first_end = temp_data[index][1]
                if index == 0:
                    if first_start > 0:
                        parts.append([0.0, first_start, 'silence'])
                if index == length-1:
                    parts.append([first_start, first_end, 'voice'])
                    if video_length != None:
                        if first_end < video_length:
                            parts.append([first_end, video_length, 'silence'])
                    break
                next_index = index + 1
                second_start = temp_data[next_index][0]
                second_end = temp_data[next_index][1]
                if (first_end <= second_start):
                    parts.append([first_start, first_end, 'voice'])
                    if (first_end < second_start):
                        parts.append([first_end, second_start, 'silence'])
                elif (first_end > second_end):
                    first_end = second_start
                    parts.append([first_start, first_end, 'voice'])
                index += 1
            return parts
        else:
            return parts

    def __get_data_from_video(self, path: str, minimum_interval_time_in_seconds: float = 0.0, video_length: float = None):
        from vosk import Model, KaldiRecognizer, SetLogLevel

        assert os.path.exists(
            path), f"source video file {path} does not exist!"

        SetLogLevel(0)
        sample_rate = 16000
        model = Model(self.vosk_model_folder.as_posix())
        rec = KaldiRecognizer(model, sample_rate)

        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                    path,
                                    '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                                   stdout=subprocess.PIPE)

        data_list = []
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if len(result.keys()) >= 2:
                    "{'result': [{'conf': 0.875663, 'end': 4.35, 'start': 4.11, 'word': 'nice'}, {'conf': 1.0, 'end': 5.13, 'start': 4.59, 'word': 'day'}], 'text': 'nice day'}"
                    start = result['result'][0]['start']
                    end = result['result'][-1]['end']
                    data_list.append({"start": start, "end": end})
            else:
                # print(rec.PartialResult())
                pass
        return self.__time_interval_filter(data_list, minimum_interval_time_in_seconds, video_length)

    def remove_silence_parts_from_videos_in_a_folder(self, source_folder: str, target_video_path: str, minimum_interval_time_in_seconds: float = 1.0, fps: int = None, resolution: Tuple[int, int] = None, preset: str = 'placebo'):
        """
        We will first concatenate the files under the source_folder into a video by created_time, then we remove those silence parts in that videoig

        Parameters
        ----------
        source_folder: string
        target_video_path: string
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        fps: int
        target_resolution: Tuple(int, int)
            Set to (desired_width, desired_height) to have ffmpeg resize the frames. Choices are: (1920, 1080), (1280, 720), (640, 480) and so on. 
        preset: string
            Sets the time that FFMPEG will spend optimizing the compression. Choices are: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo. Note that this does not impact the quality of the video, only the size of the video file.
        """
        make_sure_target_does_not_exist(target_video_path)

        video_files = [video for video in disk.get_files(
            source_folder, recursive=False)]
        video_files = disk.sort_files_by_time(video_files)
        if resolution != None:
            resolution = (resolution[1], resolution[0])
        parent_clips = [VideoFileClip(
            video, target_resolution=resolution) for video in video_files]
        length = len(video_files)
        remain_clips = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index/length*100)) + " %...")
            parts = self.__get_data_from_video(
                video_file, minimum_interval_time_in_seconds, parent_clips[index].duration)
            for part in parts:
                if part[2] == 'voice':
                    remain_clips.append(
                        parent_clips[index].subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(remain_clips)
        concat_clip.write_videofile(target_video_path, fps=fps, preset=preset)
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def speed_up_silence_parts_from_videos_in_a_folder(self, source_folder: str, target_video_path: str, speed: int = 4, minimum_interval_time_in_seconds: float = 1.0, fps: int = None, resolution: Tuple[int, int] = None, preset: str = 'placebo'):
        """
        We will first concatenate the files under the source_folder into a video by created_time, then we speed up those silence parts in that videoig

        Parameters
        ----------
        source_folder: string
        target_video_path: string
        speed: float
            how quick you want the silence parts to be
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        fps: int
        target_resolution: Tuple(int, int)
            Set to (desired_width, desired_height) to have ffmpeg resize the frames. Choices are: (1920, 1080), (1280, 720), (640, 480) and so on. 
        preset: string
            Sets the time that FFMPEG will spend optimizing the compression. Choices are: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo. Note that this does not impact the quality of the video, only the size of the video file.
        """
        make_sure_target_does_not_exist(target_video_path)

        video_files = [video for video in disk.get_files(
            source_folder, recursive=False)]
        video_files = disk.sort_files_by_time(video_files)
        if resolution != None:
            resolution = (resolution[1], resolution[0])
        parent_clips = [VideoFileClip(
            video, target_resolution=resolution) for video in video_files]
        length = len(video_files)
        remain_clips = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index/length*100)) + " %...")
            parts = self.__get_data_from_video(
                video_file, minimum_interval_time_in_seconds, parent_clips[index].duration)
            for part in parts:
                if part[2] == 'voice':
                    remain_clips.append(
                        parent_clips[index].subclip(part[0], part[1]))
                elif part[2] == 'silence':
                    remain_clips.append(
                        parent_clips[index].subclip(part[0], part[1]).without_audio().fx(
                            vfx.speedx, speed
                        )
                    )

        concat_clip = concatenate_videoclips(remain_clips)
        concat_clip.write_videofile(target_video_path, fps=fps, preset=preset)
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def remove_silence_parts_from_video(self, source_video_path: str, target_video_path: str, minimum_interval_time_in_seconds: float = 1.0):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        """
        make_sure_target_does_not_exist(target_video_path)

        parent_clip = VideoFileClip(source_video_path)
        parts = self.__get_data_from_video(
            source_video_path, minimum_interval_time_in_seconds, parent_clip.duration)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            if part[2] == 'voice':
                try:
                    time_duration = part[1] - part[0]
                    print(str(int(index/length*100))+"%,", "remain " +
                          str(int(time_duration)) + " seconds")
                except Exception as e:
                    print(e)
                clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)
        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers)
        concat_clip.close()
        parent_clip.close()

        done()

    def speedup_silence_parts_in_video(self, source_video_path: str, target_video_path: str, speed: int = 4, minimum_interval_time_in_seconds: float = 1.0, fps: int = None, resolution: Tuple[int, int] = None, preset: str = 'placebo'):
        """
        Instead remove silence, we can speed up the silence parts in a video

        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        speed: float
            how quick you want the silence parts to be
        """
        make_sure_target_does_not_exist(target_video_path)

        parent_clip = VideoFileClip(
            source_video_path, target_resolution=(resolution[1], resolution[0]))
        parts = self.__get_data_from_video(
            source_video_path, minimum_interval_time_in_seconds, parent_clip.duration)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            if part[2] == 'voice':
                clip_list.append(parent_clip.subclip(part[0], part[1]))
            elif part[2] == 'silence':
                try:
                    time_duration = part[1] - part[0]
                    print(str(int(index/length*100))+"%,", "speed up " +
                          str(int(time_duration)) + " seconds")
                except Exception as e:
                    print(e)
                clip_list.append(
                    parent_clip.subclip(part[0], part[1]).without_audio().fx(
                        vfx.speedx, speed
                    )
                )

        concat_clip = concatenate_videoclips(clip_list)
        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, fps=fps, preset=preset)
        concat_clip.close()
        parent_clip.close()

        done()


if __name__ == "__main__":
    video = DeepVideo()
    video.speedup_silence_parts_in_video(
        "/home/yingshaoxo/demo.mp4", "/home/yingshaoxo/ok.mp4", 10)
