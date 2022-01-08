import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import shutil
import datetime
import librosa
import numpy as np
import os
import math
import multiprocessing
import json

#import pyaudio
#import sys
#import wave
import subprocess

from typing import List, Tuple
from auto_everything.io import IO
from auto_everything.terminal import Terminal
from auto_everything.network import Network
from auto_everything.disk import Disk

t = Terminal(debug=True)
io_ = IO()
network = Network()
disk = Disk()


def print_split_line():
    print('\n' + '-' * 20 + '\n')


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


class VideoUtils():
    def convert_video_to_wav(self, source_video_path, target_wav_path):
        return convert_video_to_wav(source_video_path, target_wav_path)

    def get_mono_16khz_audio_array(self, sourceWavePath: str):
        y, s = librosa.load(sourceWavePath, mono=True, sr=16000)
        # s is audio sample rate
        return y, s

    def convert_array_to_batch_samples(self, y, durationInSecondsForEach=1.0):
        samplesForEachOne = librosa.time_to_samples(
            durationInSecondsForEach, sr=16000)
        num_sections = math.ceil(y.shape[0] / samplesForEachOne)
        return np.array_split(y, num_sections, axis=0)

    def get_wav_infomation(self, wav_path):
        wav_path = try_to_get_absolutely_path(wav_path)
        make_sure_source_is_absolute_path(wav_path)

        y, sr = librosa.load(wav_path, sr=None)
        return y, sr

    def merge_continues_intervals(self, intervals, thresholdInSeconds):
        # merge continues videos
        # if time betewwn two intervals are less than thresholdInSeconds, we merge them
        i = 0
        length = len(intervals)
        modified = True
        while modified == True:
            modified = False
            i = 0
            while i < len(intervals):
                if i + 1 < len(intervals):
                    A = intervals[i][1]
                    B = intervals[i + 1][0]
                    d = B - A
                    # print(d)
                    if d < thresholdInSeconds:
                        intervals[i][1] = intervals[i + 1][1]
                        del intervals[i + 1]
                        modified = True
                i += 1
        return intervals

    def drop_too_short_intervals(self, intervals, thresholdInSeconds):
        # remove too short videos
        # if the time delta in a interval is less than thresholdInSeconds, we drop it
        i = 0
        length = len(intervals)
        modified = True
        while modified == True:
            modified = False
            i = 0
            while i < len(intervals):
                A = intervals[i][0]
                B = intervals[i][1]
                d = B - A
                # print(d)
                if d < thresholdInSeconds:
                    del intervals[i]
                    i -= 1
                    modified = True
                i += 1

        return intervals

    def get_intersection_of_two_intervals(self, A, B):
        i = j = 0
        ans = []
        while i < len(A) and j < len(B):
            start_a, end_a = A[i]
            start_b, end_b = B[j]
            if start_b <= start_a <= end_b:
                ans.append([start_a, min(end_a, end_b)])
                if end_a < end_b:
                    i += 1
                else:
                    j += 1
            elif start_a <= start_b <= end_a:
                ans.append([start_b, min(end_a, end_b)])
                if end_a < end_b:
                    i += 1
                else:
                    j += 1
            elif start_a < start_b:
                i += 1
            else:
                j += 1
        return ans

    def fix_rotation(self, video):
        """
            Rotate the video based on orientation
        """
        rotation = video.rotation
        if rotation == 90:  # If video is in portrait
            video = vfx.rotate(video, -90)
        elif rotation == 270:  # Moviepy can only cope with 90, -90, and 180 degree turns
            # Moviepy can only cope with 90, -90, and 180 degree turns
            video = vfx.rotate(video, 90)
        elif rotation == 180:
            video = vfx.rotate(video, 180)
        return video


videoUtils = VideoUtils()


class AudioProcessor:
    def __init__(self):
        try:
            import pydub
            self.pydub = pydub
        except Exception as e:
            print("brew install ffmpeg")
            print("python3 -m pip install pydub")
            raise e

    def getCompleteTimeRangeForNoSilenceAndSilenceAudioSlice(self, soundObject, silence_threshold=-50):
        originalSequenceLength = len(soundObject)

        voiceNoSilenceTimeRangeList = self.pydub.silence.detect_nonsilent(
            soundObject, silence_thresh=silence_threshold)

        new_list = []

        for index, item in enumerate(voiceNoSilenceTimeRangeList):
            if index == 0:
                new_list.append([item[0], item[1], 1])
            else:
                new_list.append([item[0], item[1], 1])
                if item[0] != voiceNoSilenceTimeRangeList[index-1][1]:
                    new_list.insert(-1,
                                    [voiceNoSilenceTimeRangeList[index-1][1], item[0], 0])

        if len(new_list):
            if new_list[0][0] != 0:
                new_list.insert(0, [0, new_list[0][0], 0])
            if new_list[-1][1] != originalSequenceLength:
                new_list.append([new_list[-1][1], originalSequenceLength, 0])

        return new_list


audioProcessor = AudioProcessor()


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

    def _get_voice_parts(self, source_audio_path, top_db, minimum_interval_time_in_seconds=1.0, skip_sharp_noise=False):
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
                    noise_interval = (part[0] - parts[index - 1][1])
                    if (noise_interval > minimum_interval_samples):
                        time_gaps = (part[0] - parts[index - 1][1]) * 0.1
                        # we fear if the time_gaps is too long
                        if time_gaps >= minimum_interval_samples:
                            time_gaps = minimum_interval_samples // 2
                        new_parts.append(
                            [parts[index - 1][1],
                             parts[index - 1][1] + time_gaps
                             ]
                        )
                        new_parts.append(
                            [part[0] - time_gaps,
                             part[0]
                             ]
                        )
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index - 1][1], part[0]])
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
                    inverval = (part[0] - new_parts[index - 1][1])
                    if (inverval == 0):
                        if first == -1:
                            first = new_parts[index - 1][0]
                    else:
                        if (first == -1):
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append(
                                [first, new_parts[index - 1][1]])
                            first = -1

            final_parts.append([final_parts[-1][1], the_missing_final])

            return np.array(final_parts)

        parts = librosa.effects.split(y, top_db=top_db)  # return samples

        # parts = ignore_short_noise(parts)

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

        # parts[0] = [0, parts[0][1]]
        parts = from_samples_to_seconds(parts)

        newVersionOfParts = []

        def to_seconds(s):
            hr, min, sec = [float(x) for x in s.split(':')]
            return hr * 3600 + min * 60 + sec

        for part in parts:
            A = part[0]
            B = part[1]
            A = to_seconds(A)
            B = to_seconds(B)
            newVersionOfParts.append([A, B])

        parts = newVersionOfParts

        if skip_sharp_noise:
            parts = videoUtils.drop_too_short_intervals(parts, 0.1)  # 0.2
            parts = videoUtils.merge_continues_intervals(
                parts, thresholdInSeconds=0.5)  # 0.5

        return parts

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
                    noise_interval = (part[0] - parts[index - 1][1])
                    if (noise_interval > minimum_interval_samples):
                        new_parts.append(
                            [parts[index - 1][1], parts[index - 1][1]])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index - 1][1], part[0]])
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
                    inverval = (part[0] - new_parts[index - 1][1])
                    if (inverval == 0):
                        if first == -1:
                            first = new_parts[index - 1][0]
                    else:
                        if (first == -1):
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append(
                                [first, new_parts[index - 1][1]])
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
                    [0, from_samples_to_seconds([parts[index - 1][1], first])])
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
            all_silence += (part[0] - new_parts[index - 1][1])

        ratio = all_silence / new_parts[-1][1]
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
            index = (6 - len(str(index))) * '0' + str(index)

            target_video_path = add_path(target_folder, str(index) + ".mp4")

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

            clip_list = [videoUtils.fix_rotation(VideoFileClip(clip))
                         for clip in source_video_path_list]
            final_clip = concatenate_videoclips(clip_list)
            final_clip.write_videofile(
                target_video_path, threads=self._cpu_core_numbers, preset=preset, audio_codec="aac", verbose=False)

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

    def remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice,
                                        minimum_interval_time_in_seconds=None, voice_only=False,
                                        skip_sharp_noise=False):
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
            working_dir, disk.get_hash_of_a_path(source_video_path) + 'audio_for_remove_silence_parts_from_video.wav'))
        temp_video_path = add_path(
            working_dir, disk.get_hash_of_a_path(source_video_path) + 'temp_for_remove_silence_parts_from_video.mp4')

        if minimum_interval_time_in_seconds is None:
            parts = self._get_voice_parts(
                audio_path, top_db, skip_sharp_noise=skip_sharp_noise)
        else:
            parts = self._get_voice_parts(
                audio_path, top_db, minimum_interval_time_in_seconds, skip_sharp_noise=skip_sharp_noise)

        # """
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            try:
                time_duration = int(part[1] - part[0])
                print(str(int(index / length * 100)) + "%,",
                      "cut " + str(time_duration) + " seconds")
            except Exception as e:
                print(e)
            clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)

        if not voice_only:
            concat_clip.write_videofile(
                target_video_path, threads=self._cpu_core_numbers, audio_codec="aac", verbose=False
            )
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

    def humanly_remove_silence_parts_from_video(self, source_video_path, target_video_path,
                                                db_for_split_silence_and_voice, minimum_interval=1):
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
        audio_path = add_path(
            working_dir, 'audio_for_humanly_remove_silence_parts_from_video.wav')
        if not os.path.exists(audio_path):
            convert_video_to_wav(source_video_path, audio_path)

        temp_video_path = add_path(
            working_dir, 'temp_for_humanly_remove_silence_parts_from_video.mp4')

        try:
            # parts = self._get_voice_parts(
            #    source_audio_path=audio_path, top_db=db_for_split_silence_and_voice)
            # ratio = int(self._evaluate_voice_parts(parts) * 100)
            target_audio_path = self.remove_silence_parts_from_video(
                source_video_path, target_video_path, db_for_split_silence_and_voice=db_for_split_silence_and_voice,
                minimum_interval_time_in_seconds=minimum_interval, voice_only=True)
        except Exception as e:
            print(e)
            print()
            print(
                "You probably gave me a wroung db value, try to make it smaller and try it again")
            exit()

        make_sure_target_does_not_exist(temp_video_path)
        make_sure_target_does_not_exist(audio_path)

        os.system(f'xdg-open {target_audio_path}')

        answer = input(
            f"Are you happy with the audio file: {target_audio_path}% ? (y/n) (you may have to exit this script to hear your audio from your computers)\n")
        if answer.strip() == "y":
            print("ok, let's do it!")

            make_sure_target_does_not_exist(target_audio_path)
            self.remove_silence_parts_from_video(
                source_video_path, target_video_path, db_for_split_silence_and_voice=db_for_split_silence_and_voice,
                minimum_interval_time_in_seconds=minimum_interval)

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
        video_speed = str(float(1 / speed))[:6]

        if speed <= 4:
            parts = math.ceil(speed / 2)
            value_of_each_part = str(speed ** (1 / parts))[:6]
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

        clip = videoUtils.fix_rotation(clip)
        clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, audio_codec="aac", verbose=False)

        done()

    def speedup_silence_parts_in_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice,
                                       speed=4):
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
            working_dir, disk.get_hash_of_a_path(source_video_path) + 'audio_for_speedup_silence_parts_in_video.wav'))

        voice_and_silence_parts = self._get_voice_and_silence_parts(
            audio_path, top_db)

        make_sure_target_does_not_exist(audio_path)
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list = []
        length = len(voice_and_silence_parts)
        for index, part in enumerate(voice_and_silence_parts):
            if len(part[1][0].split(".")) < 2:
                part[1][0] += ".000000"
            try:
                time_duration = (datetime.datetime.strptime(
                    part[1][1], '%H:%M:%S.%f') - datetime.datetime.strptime(part[1][0], '%H:%M:%S.%f')).seconds
                print(str(int(index / length * 100)) + "%,", "-".join([p.split(".")[
                    0] for p in part[1]]) + ",",
                    "cut " + str(time_duration) + " seconds")
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
            target_video_path, threads=self._cpu_core_numbers, audio_codec="aac", verbose=False)
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

    def fix_corrupt_videos_in_a_folder(self, source_folder: str):
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        if not os.path.isdir(source_folder):
            raise Exception("it needs to be a folder")

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(working_dir, 'fixed_' +
                              os.path.basename(source_folder))
        if not os.path.exists(new_folder):
            os.makedirs(new_folder, exist_ok=True)

        filelist = disk.get_files(source_folder, type_limiter=[
                                  ".mp4", ".mkv", ".avi", ".rmvb", ".ts"])

        for file in filelist:
            target_video_path = file.replace(source_folder, new_folder)
            target_dir = get_directory_name(target_video_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            if not os.path.exists(target_video_path):
                try:
                    t.run(f"""
                        ffmpeg -i "{file}" -c copy {target_video_path}
                    """)
                except KeyboardInterrupt:
                    t.kill("ffmpeg")
                    t.run(f'rm "{target_video_path}"')
                    exit()

        done()

    def compress_videos_in_a_folder(self, source_folder, fps: int = 29, resolution: Tuple[int, int] = None,
                                    preset: str = 'veryslow'):
        """
        Parameters
        ----------
        source_video_path: string
        preset: string
            A preset is a collection of options that will provide a certain encoding speed to compression ratio. A slower preset will provide better compression
                ultrafast
                superfast
                veryfast
                faster
                fast
                medium – default preset
                slow
                slower
                veryslow
                placebo – ignore this as it is not useful (see FAQ)
        """
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        if not os.path.isdir(source_folder):
            raise Exception("it needs to be a folder")

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(working_dir, 'compressed_' +
                              os.path.basename(source_folder))
        if not os.path.exists(new_folder):
            os.makedirs(new_folder, exist_ok=True)

        filelist = disk.get_files(source_folder, type_limiter=[
                                  ".mp4", ".mkv", ".avi", ".rmvb", ".ts"])

        for file in filelist:
            target_video_path = file.replace(source_folder, new_folder)
            target_dir = get_directory_name(target_video_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            # make_sure_target_does_not_exist(target_video_path)
            if not os.path.exists(target_video_path):
                try:
                    if resolution:
                        t.run(f"""
                            ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale={resolution[0]}:{resolution[1]} -r {fps} -preset {preset} "{target_video_path}"
                        """)
                    else:
                        t.run(f"""
                            ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale=-2:720 -r {fps} -preset {preset} "{target_video_path}"
                        """)
                except KeyboardInterrupt:
                    t.kill("ffmpeg")
                    t.run(f'rm "{target_video_path}"')
                    exit()
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

    def removeTopAndBottomOfAVideo(self, source_video_path: str, target_video_path: str, cropRatio: int = 0.12):
        make_sure_target_does_not_exist(target_video_path)

        clip = VideoFileClip(source_video_path)
        clip = videoUtils.fix_rotation(clip)
        width = clip.w
        height = clip.h
        cropRatio = 0.12
        cropPixels = int(cropRatio * height)
        clip = clip.crop(x1=0, y1=cropPixels, x2=width, y2=height - cropPixels)
        clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, audio_codec="aac", verbose=False)

        done()

    def splitVideoToParts(self, source_video_path: str, target_video_folder: str, numOfParts: int):
        if not disk.exists(target_video_folder):
            os.mkdir(target_video_folder)

        clip = VideoFileClip(source_video_path)
        clip = videoUtils.fix_rotation(clip)
        length = clip.duration
        partLength = length / numOfParts

        clips = []
        for i in range(numOfParts):
            clips.append(clip.subclip(i * partLength, (i + 1) * partLength))

        for i, c in enumerate(clips):
            c.write_videofile(
                f"{target_video_folder}/{i}.mp4", threads=self._cpu_core_numbers, audio_codec="aac", verbose=False)

        done()

    def addMusicFilesToVideoFile(self, source_file_path: str, target_file_path: str, musicFiles: List[str], preDecreaseDBValueForTheMusic: int = 0, howManyDBYouWannaTheMusicToDecreaseWhenYouSpeak: int = 15):
        make_sure_target_does_not_exist(target_file_path)

        if not disk.exists(source_file_path):
            print("source video does not exist")
            return

        if not source_file_path.endswith(".mp4"):
            print("source video must be a mp4 file")
            return

        if any([disk.exists(file) == False for file in musicFiles]):
            print("one of the music files does not exist")
            return

        if len(musicFiles) == 0:
            print("no music file gets provided")
            return

        # handle input voice
        humanVoice = audioProcessor.pydub.AudioSegment.from_file(
            source_file_path, format="mp4")

        # handle input music
        musicSound = audioProcessor.pydub.AudioSegment.from_file(
            musicFiles[0], format="mp3")
        for musicFile in musicFiles[1:]:
            musicSound += audioProcessor.pydub.AudioSegment.from_file(
                musicFile, format="mp3")

        while len(musicSound) < len(humanVoice):
            musicSound *= 2

        musicSound = musicSound[:len(humanVoice)]
        musicSound -= preDecreaseDBValueForTheMusic

        # handle the silence
        musicSlices = []

        infoOfTheVoice = audioProcessor.getCompleteTimeRangeForNoSilenceAndSilenceAudioSlice(
            humanVoice)

        for a, b, c in infoOfTheVoice:
            music_part = musicSound[a:b]
            if c == 1:
                music_part -= howManyDBYouWannaTheMusicToDecreaseWhenYouSpeak
            musicSlices.append(music_part)

        processedMusic = musicSlices[0]
        for part in musicSlices[1:]:
            processedMusic += part

        # remix
        finalSound = humanVoice.overlay(processedMusic)
        tempMp3FilePath = disk.getATempFilePath(source_file_path)
        finalSound.export(tempMp3FilePath, format="mp3")

        # add all those sound to a video file
        videoclip = VideoFileClip(source_file_path)
        audioclip = AudioFileClip(tempMp3FilePath)

        videoclip.audio = audioclip
        videoclip.write_videofile(
            target_file_path, threads=self._cpu_core_numbers, verbose=False)

        done()


class DeepVideo():
    """
    For this one, I'll use deep learning.

    It's based on:
    1. ubuntu core
    2. vosk
    3. ffmpeg
    4. moviepy
    5. librosa
    6. pornstar
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
        self.vosk_model_folder = self.config_folder / Path("model")
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
            if index == length - 1:
                end = item['end']
            temp_data.append([start, end])
        parts = []
        index = 0
        length = len(temp_data)
        if length >= 2:
            while index <= length - 1:
                first_start = temp_data[index][0]
                first_end = temp_data[index][1]
                if index == 0:
                    if first_start > 0:
                        parts.append([0.0, first_start, 'silence'])
                if index == length - 1:
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

    def __get_raw_data_from_video(self, path: str):
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
                    """
                    {'result': 
                        [
                            {'conf': 0.875663, 'end': 4.35, 'start': 4.11, 'word': 'nice'}, 
                            {'conf': 1.0, 'end': 5.13, 'start': 4.59, 'word': 'day'}
                        ], 
                     'text': 'nice day'}
                    """
                    start = result['result'][0]['start']
                    end = result['result'][-1]['end']
                    text = result['result']["text"]
                    data_list.append(
                        {"start": start, "end": end, "text": text})
            else:
                # print(rec.PartialResult())
                pass
        return data_list

    def __get_data_from_video(self, path: str, minimum_interval_time_in_seconds: float = 0.0,
                              video_length: float = None):
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

    def remove_silence_parts_from_videos_in_a_folder(self, source_folder: str, target_video_path: str,
                                                     minimum_interval_time_in_seconds: float = 1.0, fps: int = None,
                                                     resolution: Tuple[int, int] = None, preset: str = 'placebo'):
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

        parent_clips = [videoUtils.fix_rotation(VideoFileClip(
            video, target_resolution=resolution)) for video in video_files]
        length = len(video_files)
        remain_clips = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index / length * 100)) + " %...")
            parts = self.__get_data_from_video(
                video_file, minimum_interval_time_in_seconds, parent_clips[index].duration)
            for part in parts:
                if part[2] == 'voice':
                    remain_clips.append(
                        parent_clips[index].subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(remain_clips)
        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, fps=fps, preset=preset, audio_codec="aac", verbose=False)
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def speed_up_silence_parts_from_videos_in_a_folder(self, source_folder: str, target_video_path: str, speed: int = 4,
                                                       minimum_interval_time_in_seconds: float = 1.0, fps: int = None,
                                                       resolution: Tuple[int, int] = None, preset: str = 'placebo'):
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
        parent_clips = [videoUtils.fix_rotation(VideoFileClip(
            video, target_resolution=resolution)) for video in video_files]
        length = len(video_files)
        remain_clips = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index / length * 100)) + " %...")
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
        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, fps=fps, preset=preset, audio_codec="aac", verbose=False)
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def remove_silence_parts_from_video(self, source_video_path: str, target_video_path: str,
                                        minimum_interval_time_in_seconds: float = 1.0):
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
        parent_clip = videoUtils.fix_rotation(parent_clip)
        parts = self.__get_data_from_video(
            source_video_path, minimum_interval_time_in_seconds, parent_clip.duration)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            if part[2] == 'voice':
                try:
                    time_duration = part[1] - part[0]
                    print(str(int(index / length * 100)) + "%,", "remain " +
                          str(int(time_duration)) + " seconds")
                except Exception as e:
                    print(e)
                clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)
        concat_clip.write_videofile(
            target_video_path, threads=self._cpu_core_numbers, audio_codec="aac", verbose=False)
        concat_clip.close()
        parent_clip.close()

        done()

    def speedup_silence_parts_in_video(self, source_video_path: str, target_video_path: str, speed: int = 4,
                                       minimum_interval_time_in_seconds: float = 1.0, fps: int = None,
                                       resolution: Tuple[int, int] = None, preset: str = 'placebo'):
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

        parent_clip = videoUtils.fix_rotation(parent_clip)
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
                    print(str(int(index / length * 100)) + "%,", "speed up " +
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
            target_video_path, threads=self._cpu_core_numbers, fps=fps, preset=preset, audio_codec="aac", verbose=False)
        concat_clip.close()
        parent_clip.close()

        done()

    def _get_sounds_parts(self, source_audio_path, top_db):
        y, sr = get_wav_infomation(source_audio_path)
        parts = librosa.effects.split(y, top_db=top_db)  # return samples

        def from_samples_to_seconds(parts):
            parts = librosa.core.samples_to_time(parts, sr)  # return seconds
            new_parts = []

            for part in parts:
                part1 = part[0]
                part2 = part[1]
                new_parts.append([part1, part2])

            return new_parts

        parts[0] = [0, parts[0][1]]
        parts = from_samples_to_seconds(parts)

        return parts[1:]

    def blurPornGraphs(self, source_video_path: str, target_video_path: str):
        # useless
        import pornstar

        def doit(frame):
            if pornstar.store.nsfw_detector.isPorn(frame, 0.9):
                classList, ScoreList, PositionList = pornstar.my_object_detector.detect(
                    frame)
                if "person" in classList:
                    frame = pornstar.effect_of_blur(frame, kernel=30)
            return frame

        pornstar.process_video(path_of_video=source_video_path,
                               effect_function=doit, save_to=target_video_path)


if __name__ == "__main__":
    video = Video()
    video.compress_videos_in_a_folder("/home/yingshaoxo/Videos/doing", fps=15)
