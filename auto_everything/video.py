import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip #type: ignore
import shutil
import datetime
import librosa
import numpy as np
import os
import math
import multiprocessing
import json

# import pyaudio
# import sys
# import wave
import subprocess

# import torchaudio
# import torch
# from speechbrain.dataio.dataio import read_audio
from speechbrain.pretrained import SepformerSeparation as separator

from typing import Any, List, Tuple

from auto_everything.io import IO
from auto_everything.terminal import Terminal
from auto_everything.network import Network
from auto_everything.disk import Disk
from auto_everything.audio import DeepAudio

t = Terminal(debug=True)
io_ = IO()
network = Network()
disk = Disk()
deep_audio = DeepAudio()



def string_to_timedelta(text: str):
    """
    input: '0:00:16.648707'
    """
    t = datetime.datetime.strptime(text, '%H:%M:%S.%f')
    delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
    return delta

# def seconds_to_string_format(num):
#     """
#     output: '0:00:16.648707'
#     """
#     return str(datetime.timedelta(seconds=num))

def print_split_line():
    print("\n" + "-" * 20 + "\n") #type: ignore


def done():
    print_split_line()
    print("We are done, sir.")
    print_split_line()


def get_directory_name(path: str):
    return os.path.dirname(path)


def add_path(path1: str, path2: str):
    return os.path.join(path1, path2)


def try_to_get_absolutely_path(path: str):
    abs_path = os.path.abspath(path)
    if os.path.isabs(abs_path) or os.path.exists(abs_path):
        return abs_path
    else:
        return path


def make_sure_source_is_absolute_path(path: str | list[str]):
    path_list: list[str] = []
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


def make_sure_target_is_absolute_path(path: str | list[str]):
    path_list: list[str] = []
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


def make_sure_target_does_not_exist(path: str | list[str]):
    path_list: list[str] = []
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
                        f"I can't remove target '{p}' for you, please check your permission"
                    )
                    exit()


def convert_video_to_wav(source_video_path: str, target_wav_path: str, sample_rate:str|int|None=None):
    source_video_path = try_to_get_absolutely_path(source_video_path)
    make_sure_source_is_absolute_path(source_video_path)
    target_wav_path = try_to_get_absolutely_path(target_wav_path)
    make_sure_target_is_absolute_path(target_wav_path)

    make_sure_target_does_not_exist(target_wav_path)

    if sample_rate == None:
        t.run(
            f"""
            ffmpeg -i "{source_video_path}" "{target_wav_path}"
            """
        )
    else:
        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -vn -acodec pcm_s16le -ar {sample_rate} -ac 2 "{target_wav_path}"
            """
        )

    return target_wav_path


def get_wav_infomation(wav_path: str) -> tuple[np.ndarray[Any, Any], int]:
    wav_path = try_to_get_absolutely_path(wav_path)
    make_sure_source_is_absolute_path(wav_path)

    y, sr = librosa.load(wav_path) #type: ignore 
    return y, sr #type: ignore


class VideoUtils:
    def convert_video_to_wav(self, source_video_path: str, target_wav_path: str):
        return convert_video_to_wav(source_video_path, target_wav_path)

    def get_mono_16khz_audio_array(self, sourceWavePath: str) -> tuple[np.ndarray[Any, Any], int]:
        y, s = librosa.load(sourceWavePath, mono=True, sr=16000)  #type: ignore
        # s is audio sample rate
        return y, s  #type: ignore

    def convert_array_to_batch_samples(self, y: np.ndarray[Any, Any], durationInSecondsForEach:float=1.0) -> list[np.ndarray[Any, Any]]:
        samplesForEachOne = librosa.time_to_samples(durationInSecondsForEach, sr=16000) #type: ignore
        num_sections = math.ceil(y.shape[0] / samplesForEachOne) #type: ignore
        return np.array_split(y, num_sections, axis=0) #type: ignore

    def get_wav_infomation(self, wav_path: str) -> tuple[np.ndarray[Any, Any], int]:
        wav_path = try_to_get_absolutely_path(wav_path)
        make_sure_source_is_absolute_path(wav_path)

        y, sr = librosa.load(wav_path) #type: ignore
        return y, sr #type: ignore

    def merge_continues_intervals(self, intervals: list[Any], thresholdInSeconds: float | int):
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

    def drop_too_short_intervals(self, intervals: list[Any], thresholdInSeconds: float | int):
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

    def get_intersection_of_two_intervals(self, A: list[Any], B: list[Any]):
        i = j = 0
        ans: list[Any] = []
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

    def fix_rotation(self, video: Any):
        """
        Rotate the video based on orientation
        """
        try:
            rotation = video.rotation
            if rotation == 90:  # If video is in portrait
                video = vfx.rotate(video, -90)  # type: ignore
            elif (
                rotation == 270
            ):  # Moviepy can only cope with 90, -90, and 180 degree turns
                # Moviepy can only cope with 90, -90, and 180 degree turns
                video = vfx.rotate(video, 90)  # type: ignore
            elif rotation == 180:
                video = vfx.rotate(video, 180)  # type: ignore
            return video
        except Exception as e:
            print(e)
            return video


videoUtils = VideoUtils()


class AudioProcessor:
    def __init__(self):
        try:
            import pydub
            import pydub.silence

            self.pydub = pydub
        except Exception as e:
            print("brew install ffmpeg")
            print("python3 -m pip install pydub")
            raise e

    def getCompleteTimeRangeForNoSilenceAndSilenceAudioSlice(
        self, soundObject: Any, silence_threshold:int=-50
    ):
        originalSequenceLength = len(soundObject)

        voiceNoSilenceTimeRangeList = self.pydub.silence.detect_nonsilent( #type: ignore
            soundObject, silence_thresh=silence_threshold
        )

        new_list: list[Any] = []
        for index, item in enumerate(voiceNoSilenceTimeRangeList): #type: ignore
            if index == 0:
                new_list.append([item[0], item[1], 1])
            else:
                new_list.append([item[0], item[1], 1])
                if item[0] != voiceNoSilenceTimeRangeList[index - 1][1]:
                    new_list.insert(
                        -1, [voiceNoSilenceTimeRangeList[index - 1][1], item[0], 0]
                    )

        if len(new_list):
            if new_list[0][0] != 0:
                new_list.insert(0, [0, new_list[0][0], 0])
            if new_list[-1][1] != originalSequenceLength:
                new_list.append([new_list[-1][1], originalSequenceLength, 0])

        return new_list


audioProcessor = AudioProcessor()


# we'll use ffmpeg to do the real work
class Video:
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

    def _get_voice_parts(
        self,
        source_audio_path: str,
        top_db: int,
        minimum_interval_time_in_seconds: float | int=1.0,
        skip_sharp_noise: bool=False,
    ):
        y, sr = get_wav_infomation(source_audio_path)
        minimum_interval_samples: np.ndarray[Any, Any] = librosa.core.time_to_samples( #type: ignore
            minimum_interval_time_in_seconds, sr=sr
        )

        def ignore_short_noise(parts: list[Any]) -> Any:
            # ignore short noise
            new_parts: list[Any] = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = part[0] - parts[index - 1][1]
                    if noise_interval > minimum_interval_samples:
                        time_gaps = (part[0] - parts[index - 1][1]) * 0.1
                        # we fear if the time_gaps is too long
                        if time_gaps >= minimum_interval_samples:
                            time_gaps = minimum_interval_samples // 2
                        new_parts.append(
                            [parts[index - 1][1], parts[index - 1][1] + time_gaps]
                        )
                        new_parts.append([part[0] - time_gaps, part[0]])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index - 1][1], part[0]])
                        new_parts.append(list(part))

            the_missing_final = new_parts[-1][1]
            # combine continuous voice
            final_parts: list[Any] = []
            first = -1
            for index, part in enumerate(new_parts):
                if index == 0:
                    final_parts.append(part)
                    continue
                else:
                    inverval = part[0] - new_parts[index - 1][1]
                    if inverval == 0:
                        if first == -1:
                            first = new_parts[index - 1][0]
                    else:
                        if first == -1:
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append([first, new_parts[index - 1][1]])
                            first = -1

            final_parts.append([final_parts[-1][1], the_missing_final])

            return np.array(final_parts) #type: ignore

        parts = librosa.effects.split(y, top_db=top_db) #type: ignore  # return samples

        # parts = ignore_short_noise(parts)

        # new_y = librosa.effects.remix(self._y, parts) # receive samples
        # target_file_path = os.path.join(self._video_directory, "new_" + self._audio_name)
        # if t.exists(target_file_path):
        #    os.remove(target_file_path)
        # librosa.output.write_wav(target_file_path, new_y, self._sr)

        def from_samples_to_seconds(parts: Any):
            parts = librosa.core.samples_to_time(parts, sr=sr)  # return seconds #type: ignore

            def seconds_to_string_format(num: int | float):
                return str(datetime.timedelta(seconds=num))

            new_parts: list[Any] = []
            for part in parts:
                part1 = seconds_to_string_format(part[0])
                part2 = seconds_to_string_format(part[1])
                new_parts.append([part1, part2])
            return new_parts

        # parts[0] = [0, parts[0][1]]
        parts = from_samples_to_seconds(parts)

        def to_seconds(s: str):
            hr, min, sec = [float(x) for x in s.split(":")]
            return hr * 3600 + min * 60 + sec

        newVersionOfParts: list[Any] = []
        for part in parts:
            a_ = part[0]
            b_ = part[1]
            a_ = to_seconds(a_)
            b_ = to_seconds(b_)
            newVersionOfParts.append([a_, b_])

        parts = newVersionOfParts

        if skip_sharp_noise:
            parts = videoUtils.drop_too_short_intervals(parts, 0.1)  # 0.2
            parts = videoUtils.merge_continues_intervals(
                parts, thresholdInSeconds=0.5
            )  # 0.5

        return parts

    def _get_voice_and_silence_parts(
        self, source_audio_path: str, top_db: int, minimum_interval_time_in_seconds:float | int=1.7
    ):
        # let's assume 1=voice, 0=noise
        y, sr = get_wav_infomation(source_audio_path)
        minimum_interval_samples = librosa.core.time_to_samples( #type: ignore
            minimum_interval_time_in_seconds, sr=sr
        )

        parts = librosa.effects.split(y, top_db=top_db)  # return samples #type: ignore

        def ignore_short_noise(parts: list[Any]):
            # ignore short noise
            new_parts: list[Any] = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = part[0] - parts[index - 1][1]
                    if noise_interval > minimum_interval_samples:
                        new_parts.append([parts[index - 1][1], parts[index - 1][1]])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index - 1][1], part[0]])
                        new_parts.append(list(part))

            the_missing_final = new_parts[-1][1]
            # combine continuous voice
            final_parts: list[Any] = []
            first = -1
            for index, part in enumerate(new_parts):
                if index == 0:
                    final_parts.append(part)
                    continue
                else:
                    inverval = part[0] - new_parts[index - 1][1]
                    if inverval == 0:
                        if first == -1:
                            first = new_parts[index - 1][0]
                    else:
                        if first == -1:
                            final_parts.append([part[0], part[1]])
                        else:
                            final_parts.append([first, new_parts[index - 1][1]])
                            first = -1

            final_parts.append([final_parts[-1][1], the_missing_final])

            return np.array(final_parts) #type: ignore

        parts = ignore_short_noise(parts)
        parts = parts[1:]

        def from_samples_to_seconds(part: Any):
            part = librosa.core.samples_to_time(part, sr=sr)  # return seconds #type: ignore

            def seconds_to_string_format(num: int | float):
                return str(datetime.timedelta(seconds=num))

            return [
                seconds_to_string_format(part[0]),
                seconds_to_string_format(part[1]),
            ]

        voice_and_silence_parts: list[Any] = []
        for index, part in enumerate(parts):
            first = part[0]
            second = part[1]
            if index == 0:
                if first != 0:
                    voice_and_silence_parts.append(
                        [0, from_samples_to_seconds([0, first])]
                    )
                    voice_and_silence_parts.append(
                        [1, from_samples_to_seconds([first, second])]
                    )
            else:
                voice_and_silence_parts.append(
                    [0, from_samples_to_seconds([parts[index - 1][1], first])]
                )
                voice_and_silence_parts.append(
                    [1, from_samples_to_seconds([first, second])]
                )

        def remove_unwanted_parts(voice_and_silence_parts: list[Any]):
            return [
                part for part in voice_and_silence_parts if part[1][0] != part[1][1]
            ]

        voice_and_silence_parts = remove_unwanted_parts(voice_and_silence_parts)
        return voice_and_silence_parts

    def _get_voice_and_silence_parts_2(
        self, source_audio_path: str, top_db: int, the_maximum_silent_interval_time_in_seconds_you_wish_to_have:int|float|None=None
    ):
        """
            let's assume 1=voice, 0=silence

            ```
            return [
                [1, start_time_1, end_time_1],
                [0, start_time_2, end_time_2]
            ]
            ```

            > start_time_1 = str(datetime.timedelta(seconds=num))
        """
        y, sr = get_wav_infomation(source_audio_path)

        if the_maximum_silent_interval_time_in_seconds_you_wish_to_have == None or the_maximum_silent_interval_time_in_seconds_you_wish_to_have == 0:
            the_maximum_silent_interval_time_frames = None
        else:
            the_maximum_silent_interval_time_frames = librosa.core.time_to_samples( #type: ignore
                the_maximum_silent_interval_time_in_seconds_you_wish_to_have, sr=sr
            )

        parts = librosa.effects.split(y, top_db=top_db) # return non-silent parts #type: ignore
        #intervals[i] == (start_i, end_i) are the start and end time (in samples) of non-silent interval.

        def final_process(parts: Any): # here the simples are actually frames, which is int numbers from 0 to n
            if len(parts) == 0:
                return parts.reshape((-1, 3))

            #skip small silent intervals
            if the_maximum_silent_interval_time_frames != None:
                new_parts = np.empty_like(parts)
                for index, part in enumerate(parts):
                    if part[0] == 0:
                        frames_distance = part[2] - part[1]
                        if frames_distance <= the_maximum_silent_interval_time_frames:
                            part[0] = 1
                    new_parts[index] = part
                parts = new_parts
                #print(parts)

                new_parts = np.empty_like(parts)
                new_parts = np.delete(new_parts, np.s_[:], 0) #type: ignore
                real_index = 0
                for index, part in enumerate(parts):
                    if index < real_index:
                        continue
                    if part[0] == 1:
                        i = index
                        temp_start = part[1]
                        temp_end = part[2]
                        meet_end = True
                        while i < len(parts):
                            temp_part = parts[i]
                            if temp_part[0] == 1:
                                temp_end = temp_part[2]
                            else:
                                new_parts = np.append(new_parts, [[1, temp_start, temp_end]], axis=0) #type: ignore
                                real_index = i 
                                meet_end = False 
                                break
                            i += 1
                        if meet_end == True:
                            new_parts = np.append(new_parts, [[1, temp_start, temp_end]], axis=0) #type: ignore
                            break
                    else:
                        new_parts = np.append(new_parts, [part], axis=0) #type: ignore
                parts = new_parts
                #print(parts)

            #from_samples_to_seconds_2
            def seconds_to_string_format(num: int | float):
                return str(datetime.timedelta(seconds=num))

            #print(parts[:, 1:])
            interval_parts = librosa.core.samples_to_time(parts[:, 1:], sr=sr)  # return seconds #type: ignore
            # print(interval_parts)
            interval_parts = interval_parts.reshape((-1, 2)) #type: ignore
            # print(interval_parts)

            new_interval_parts = np.array([], dtype=object) #type: ignore
            for interval_part in interval_parts: #type: ignore
                interval_part_1 = seconds_to_string_format(interval_part[0]) #type: ignore
                interval_part_2 = seconds_to_string_format(interval_part[1]) #type: ignore
                new_interval_parts = np.append(new_interval_parts, [interval_part_1, interval_part_2]) #type: ignore
            new_interval_parts = new_interval_parts.reshape((-1, 2))

            return np.concatenate((parts[:, :1], new_interval_parts), axis=1).reshape((-1, 3)) #type: ignore

        global_start = 0
        global_end = len(y)

        result = np.array([[1, 1, 2]]) #type: ignore
        result = np.delete(result, 0, axis=0) #type: ignore
        if len(parts) > 0:
            start, end = parts[0]
            if start > global_start:
                result = np.append(result, [[0, global_start, start]], axis=0) #type: ignore
            result = np.append(result, [[1, start, end]], axis=0) #type: ignore
            previous_start, previous_end = start, end
            for index, part in enumerate(parts[1:]):
                start, end = part
                if index != len(parts) - 2:
                    # not the end
                    result = np.append(result, [[0, previous_end, start]], axis=0) #type: ignore
                    result = np.append(result, [[1, start, end]], axis=0) #type: ignore
                    previous_start, previous_end = start, end
                else:
                    # the end
                    result = np.append(result, [[0, previous_end, start]], axis=0) #type: ignore
                    result = np.append(result, [[1, start, end]], axis=0) #type: ignore
                    if end < global_end:
                        result = np.append(result, [[0, end, global_end]], axis=0) #type: ignore
            return final_process(result)
        elif len(parts) == 0:
            if len(y) == 0:
                return final_process(result)
            else:
                return final_process([[0, global_start, global_end]])
        else:
            # never possible unless librosa has bug
            return  final_process(result)

    def _evaluate_voice_parts(self, parts: list[Any]):
        from dateutil.parser import parse

        new_parts: list[Any] = []
        start_timestamp = 0
        for part in parts:
            part1 = parse(part[0]).timestamp()
            part2 = parse(part[1]).timestamp()
            if start_timestamp == 0:
                start_timestamp = part1
            new_parts.append([part1 - start_timestamp, part2 - start_timestamp])

        all_silence = 0
        for index, part in enumerate(new_parts):
            if index == 0:
                continue
            all_silence += part[0] - new_parts[index - 1][1]

        ratio = all_silence / new_parts[-1][1]
        return ratio

    def split_video_by_time_part(self, source_video_path: str, target_video_path: str, part: list[Any]):
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

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -ss {time_start} -to {time_end} -threads 8 "{target_video_path}"
        """
        )

        done()

    def _split_video_to_parts_by_time_intervals(
        self, source_video_path: str, target_folder: str, time_intervals: list[Any]
    ):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_folder)

        make_sure_target_does_not_exist(target_folder)
        if not t.exists(target_folder):
            os.mkdir(target_folder)

        for index, part in enumerate(time_intervals):
            index = (6 - len(str(index))) * "0" + str(index)

            target_video_path = add_path(target_folder, str(index) + ".mp4")

            self.split_video_by_time_part(source_video_path, target_video_path, part)

        done()

    def link_videos(
        self, source_video_path_list: list[str], target_video_path: str, method:int=2, preset:str="ultrafast"
    ):
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
        source_video_path_list = [
            try_to_get_absolutely_path(f) for f in source_video_path_list
        ]
        make_sure_source_is_absolute_path(source_video_path_list)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_target_is_absolute_path(target_video_path)

        if method == 1:
            working_dir = get_directory_name(target_video_path)
            txt_file_path = add_path(working_dir, "temp_list.txt")
            text = ""
            for file_path in source_video_path_list:
                text += "file " + f"'{file_path}'" + "\n"
            io_.write(txt_file_path, text)

            make_sure_target_does_not_exist(target_video_path)

            combine_command = (
                f"ffmpeg -f concat -safe 0 -i '{txt_file_path}' '{target_video_path}'"
            )
            t.run(combine_command, wait=True)

            make_sure_target_does_not_exist(txt_file_path)
        elif method == 2:
            # for the stupid moviepy library, it will case memory leak if you give it too much videos
            print(source_video_path_list)

            clip_list = [
                videoUtils.fix_rotation(VideoFileClip(clip))
                for clip in source_video_path_list
            ]
            final_clip = concatenate_videoclips(clip_list)
            final_clip.write_videofile(
                target_video_path,
                threads=self._cpu_core_numbers,
                preset=preset,
                audio_codec="aac",
                verbose=False,
            )

            for clip in clip_list:
                clip.close()
                del clip

            del final_clip

        done()

    def combine_all_mp4_in_a_folder(
        self, source_folder: str, target_video_path: str, sort_by_time:bool=True, method:int=1
    ):
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
        filelist = [
            os.path.join(source_folder, f)
            for f in os.listdir(source_folder)
            if f.endswith(".mp4")
        ]

        if sort_by_time is False:
            filelist = list(sorted(filelist))
        else:
            filelist.sort(key=lambda x: os.path.getmtime(x))

        self.link_videos(
            source_video_path_list=filelist,
            target_video_path=target_video_path,
            method=method,
        )

        if sort_by_time is False:
            make_sure_target_does_not_exist(source_folder)

        done()

    def remove_noise_from_video(
        self,
        source_video_path:str,
        target_video_path:str,
        degree:float=0.21,
        noise_capture_length:str|None=None,
    ):
        """
        Just as said, remove noise from video
        """
        degree = str(degree) # type: ignore

        source_video_path = try_to_get_absolutely_path(source_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_target_is_absolute_path(target_video_path)

        if not noise_capture_length:
            noise_capture_length = "1"
        else:
            noise_capture_length = str(noise_capture_length)

        working_dir = get_directory_name(target_video_path)

        audio_path = convert_video_to_wav(
            source_video_path,
            add_path(working_dir, "audio_for_remove_noise_from_video.wav"),
        )
        noise_sample_wav_path = add_path(working_dir, "noise_sample_wav.wav")
        noise_prof_path = add_path(working_dir, "noise_prof.prof")
        no_noise_wav_path = add_path(working_dir, "no_noise_wav.wav")
        loudnorm_wav_path = add_path(working_dir, "loudnorm_wav.wav")

        make_sure_target_does_not_exist(target_video_path)
        make_sure_target_does_not_exist(
            [
                noise_sample_wav_path,
                noise_prof_path,
                no_noise_wav_path,
                loudnorm_wav_path,
            ]
        )

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -acodec pcm_s16le -ar 128k -vn -ss 00:00:00.0 -t 00:00:0{noise_capture_length}.0 "{noise_sample_wav_path}"
        """
        )

        t.run(
            f"""
            sox "{noise_sample_wav_path}" -n noiseprof "{noise_prof_path}"
        """
        )

        t.run(
            f"""
            sox "{audio_path}" "{no_noise_wav_path}" noisered "{noise_prof_path}" {degree}
        """
        )

        t.run(
            f"""
            ffmpeg -i "{no_noise_wav_path}" -af loudnorm=I=-23:LRA=1 -ar 48000 "{loudnorm_wav_path}"
        """
        )

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -i "{loudnorm_wav_path}" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k "{target_video_path}"
        """
        )

        make_sure_target_does_not_exist(
            [
                audio_path,
                noise_sample_wav_path,
                noise_prof_path,
                no_noise_wav_path,
                loudnorm_wav_path,
            ]
        )

        done()

    def remove_silence_parts_from_video(
        self,
        source_video_path: str,
        target_video_path: str,
        db_for_split_silence_and_voice: int=40,
        minimum_interval_time_in_seconds: float|None=None,
        voice_only:bool=False,
        skip_sharp_noise:bool=False,
    ):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`, but for some case if the volume is too small, `30` would be fine
        minimum_interval_time_in_seconds: float
            any silent part longer than this value, we will remove it
        voice_only: bool
            if true, it only returns the path of silence removed mp3 file
        """

        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(
            source_video_path,
            add_path(
                working_dir,
                disk.get_hash_of_a_path(source_video_path)
                + "audio_for_remove_silence_parts_from_video.wav",
            ),
        )
        temp_video_path = add_path(
            working_dir,
            disk.get_hash_of_a_path(source_video_path)
            + "temp_for_remove_silence_parts_from_video.mp4",
        )

        if minimum_interval_time_in_seconds is None:
            parts = self._get_voice_parts(
                audio_path, top_db, skip_sharp_noise=skip_sharp_noise
            )
        else:
            parts = self._get_voice_parts(
                audio_path,
                top_db,
                minimum_interval_time_in_seconds,
                skip_sharp_noise=skip_sharp_noise,
            )

        # """
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list: list[Any] = []
        length = len(parts)
        for index, part in enumerate(parts):
            try:
                time_duration = int(part[1] - part[0])
                print(
                    str(int(index / length * 100)) + "%,",
                    "cut " + str(time_duration) + " seconds",
                )
            except Exception as e:
                print(e)
            clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)

        if not voice_only:
            concat_clip.write_videofile(
                target_video_path,
                threads=self._cpu_core_numbers,
                audio_codec="aac",
                verbose=False,
            )
            concat_clip.close()
            del concat_clip
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
            done()
            return target_video_path
        else:
            if len(target_video_path.split(".")) >= 2:
                target_audio_path = ".".join(target_video_path.split(".")[:-1]) + ".mp3"
            else:
                target_audio_path = target_video_path + ".mp3"
            make_sure_target_does_not_exist(target_audio_path)
            if concat_clip.audio != None: #type: ignore
                concat_clip.audio.write_audiofile(target_audio_path, fps=44100) #type: ignore
            else:
                raise Exception("Wrong, concat_clip.audio shouldn't be none")
            concat_clip.close()
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
            done()
            return target_audio_path

    def remove_silence_parts_from_video_2(
        self,
        source_video_path: str,
        target_video_path: str,
        db_for_split_silence_and_voice: int=40,
        the_maximum_silent_interval_time_in_seconds_you_wish_to_have: float=1.5,
        voice_only: bool=False,
    ):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`, but for some case if the volume is too small, `30` would be fine
        the_maximum_silent_interval_time_in_seconds_you_wish_to_have: float
            any silent part longer than this value, we will remove it
        voice_only: bool
            if true, it only returns the path of silence removed mp3 file
        """

        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(
            source_video_path,
            add_path(
                working_dir,
                disk.get_hash_of_a_path(source_video_path)
                + "audio_for_remove_silence_parts_from_video.wav",
            ),
        )
        temp_video_path = add_path(
            working_dir,
            disk.get_hash_of_a_path(source_video_path)
            + "temp_for_remove_silence_parts_from_video.mp4",
        )

        parts = self._get_voice_and_silence_parts_2(audio_path, top_db, the_maximum_silent_interval_time_in_seconds_you_wish_to_have)
        # print(parts)
        # print(parts.shape)
        only_voice_filter = np.apply_along_axis(lambda element : element[0] == 1, 1, parts) #type: ignore
        # print(only_voice_filter)
        parts = parts[only_voice_filter]
        parts = parts[:, 1:].tolist() # type: ignore
        # parts = np.squeeze(parts, axis=1).tolist()

        # """
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list: list[str] = []
        length = len(parts)
        for index, part in enumerate(parts):
            # part: ['0:00:09.055782', '0:00:09.822041']
            try:
                time_duration = int(
                    (string_to_timedelta(part[1]) - string_to_timedelta(part[0])).seconds
                )
                print(
                    str(int(index / length * 100)) + "%,",
                    "cut " + str(time_duration) + " seconds",
                )
            except Exception as e:
                print(e)
            clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)

        if not voice_only:
            concat_clip.write_videofile(
                target_video_path,
                threads=self._cpu_core_numbers,
                audio_codec="aac",
                verbose=False,
            )
            concat_clip.close()
            del concat_clip
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
        else:
            if len(target_video_path.split(".")) >= 2:
                target_audio_path = ".".join(target_video_path.split(".")[:-1]) + ".mp3"
            else:
                target_audio_path = target_video_path + ".mp3"
            make_sure_target_does_not_exist(target_audio_path)
            if concat_clip.audio != None: #type: ignore
                concat_clip.audio.write_audiofile(target_audio_path, fps=44100) #type: ignore
            else:
                raise Exception("Wrong, concat_clip.audio shouldn't be none")
            concat_clip.close()
            make_sure_target_does_not_exist(audio_path)
            make_sure_target_does_not_exist(temp_video_path)
            return target_audio_path

        done()

    def humanly_remove_silence_parts_from_video(
        self,
        source_video_path: str,
        target_video_path: str,
        db_for_split_silence_and_voice: int,
        minimum_interval:float | int=1,
    ):
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
            working_dir, "audio_for_humanly_remove_silence_parts_from_video.wav"
        )
        if not os.path.exists(audio_path):
            convert_video_to_wav(source_video_path, audio_path)

        temp_video_path = add_path(
            working_dir, "temp_for_humanly_remove_silence_parts_from_video.mp4"
        )

        try:
            # parts = self._get_voice_parts(
            #    source_audio_path=audio_path, top_db=db_for_split_silence_and_voice)
            # ratio = int(self._evaluate_voice_parts(parts) * 100)
            target_audio_path = self.remove_silence_parts_from_video(
                source_video_path,
                target_video_path,
                db_for_split_silence_and_voice=db_for_split_silence_and_voice,
                minimum_interval_time_in_seconds=minimum_interval,
                voice_only=True,
            )
        except Exception as e:
            print(e)
            print()
            print(
                "You probably gave me a wroung db value, try to make it smaller and try it again"
            )
            exit()

        make_sure_target_does_not_exist(temp_video_path)
        make_sure_target_does_not_exist(audio_path)

        os.system(f"xdg-open {target_audio_path}")

        answer = input(
            f"Are you happy with the audio file: {target_audio_path}% ? (y/n) (you may have to exit this script to hear your audio from your computers)\n"
        )
        if answer.strip() == "y":
            print("ok, let's do it!")

            make_sure_target_does_not_exist(target_audio_path)
            self.remove_silence_parts_from_video(
                source_video_path,
                target_video_path,
                db_for_split_silence_and_voice=db_for_split_silence_and_voice,
                minimum_interval_time_in_seconds=minimum_interval,
            )

            done()
        else:
            print()
            print("you may want to change the db, and try again.")
            exit()

    def speedup_video(self, source_video_path: str, target_video_path: str, speed:float=1.5):
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
                [f"atempo={value_of_each_part}" for i in range(parts)]
            )

            t.run(
                f"""
                ffmpeg -i "{source_video_path}" -filter_complex "[0:v]setpts={video_speed}*PTS[v];[0:a]{audio_speed}[a]" -map "[v]" -map "[a]" "{target_video_path}"
            """
            )

            done()
        else:
            self._speedup_video_with_moviepy( #type: ignore
                source_video_path, target_video_path, speed=int(speed)
            )

    def _speedup_video_with_moviepy(
        self, source_video_path: str, target_video_path: str, speed: int=4
    ):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        clip = VideoFileClip(source_video_path).without_audio().fx(vfx.speedx, speed)  # type: ignore

        clip = videoUtils.fix_rotation(clip)
        clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            audio_codec="aac",
            verbose=False,
        )

        done()

    def speedup_silence_parts_in_video(
        self,
        source_video_path: str,
        target_video_path: str,
        db_for_split_silence_and_voice: int,
        speed: int=4,
    ):
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
        audio_path = convert_video_to_wav(
            source_video_path,
            add_path(
                working_dir,
                disk.get_hash_of_a_path(source_video_path)
                + "audio_for_speedup_silence_parts_in_video.wav",
            ),
        )

        voice_and_silence_parts = self._get_voice_and_silence_parts(audio_path, top_db)

        make_sure_target_does_not_exist(audio_path)
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list: list[Any] = []
        length = len(voice_and_silence_parts)
        for index, part in enumerate(voice_and_silence_parts):
            if len(part[1][0].split(".")) < 2:
                part[1][0] += ".000000"
            try:
                time_duration = (
                    datetime.datetime.strptime(part[1][1], "%H:%M:%S.%f")
                    - datetime.datetime.strptime(part[1][0], "%H:%M:%S.%f")
                ).seconds
                print(
                    str(int(index / length * 100)) + "%,",
                    "-".join([p.split(".")[0] for p in part[1]]) + ",",
                    "cut " + str(time_duration) + " seconds",
                )
            except Exception as e:
                print(e)
            if part[0] == 1:  # voice
                clip_list.append(parent_clip.subclip(part[1][0], part[1][1]))
            else:  # silence
                clip_list.append(
                    parent_clip.subclip(part[1][0], part[1][1])
                    .without_audio()
                    .fx(vfx.speedx, speed)  # type: ignore
                )

        concat_clip = concatenate_videoclips(clip_list)

        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        del concat_clip

        done()

    def speedup_silence_parts_in_video_2(
        self,
        source_video_path: str,
        target_video_path: str,
        db_for_split_silence_and_voice: int,
        speed: int=4,
        silent_speedup_part: bool=True,
        the_maximum_silent_interval_time_in_seconds_you_wish_to_have: float=1.7
    ):
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
        audio_path = convert_video_to_wav(
            source_video_path,
            add_path(
                working_dir,
                disk.get_hash_of_a_path(source_video_path)
                + "audio_for_speedup_silence_parts_in_video.wav",
            ),
        )

        voice_and_silence_parts = self._get_voice_and_silence_parts_2(audio_path, top_db, the_maximum_silent_interval_time_in_seconds_you_wish_to_have)

        make_sure_target_does_not_exist(audio_path)
        parent_clip = VideoFileClip(source_video_path)
        parent_clip = videoUtils.fix_rotation(parent_clip)
        clip_list: list[Any] = []
        length = len(voice_and_silence_parts)
        for index, part in enumerate(voice_and_silence_parts):
            try:
                time_duration = (
                    datetime.datetime.strptime(part[2], "%H:%M:%S.%f")
                    - datetime.datetime.strptime(part[1], "%H:%M:%S.%f")
                ).seconds
                print(
                    str(int(index / length * 100)) + "%,",
                    # "-".join([p.split(".")[0] for p in part[1:]]) + ",",
                    "cut " + str(time_duration) + " seconds",
                )
            except Exception as e:
                print(e)
            if part[0] == 1:  # voice
                clip_list.append(parent_clip.subclip(part[1], part[2]))
            else:  # silence
                if silent_speedup_part:
                    clip_list.append(
                        parent_clip.subclip(part[1], part[2])
                        .without_audio()
                        .fx(vfx.speedx, speed)  # type: ignore
                    )
                else:
                    clip_list.append(
                        parent_clip.subclip(part[1], part[2])
                        .fx(vfx.speedx, speed)  # type: ignore
                    )

        concat_clip = concatenate_videoclips(clip_list)

        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        del concat_clip

        done()

    def replace_video_with_a_picture(
        self, source_video_path: str, target_video_path: str, picture: str
    ):
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

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -i "{picture}" -filter_complex "[1][0]scale2ref[i][v];[v][i]overlay" -c:a copy "{target_video_path}"
        """
        )

        done()

    def get_audio_from_video(self, source_video_path: str, target_audio_path: str):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_audio_path = try_to_get_absolutely_path(target_audio_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_audio_path)
        make_sure_target_does_not_exist(target_audio_path)

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" "{target_audio_path}"
        """
        )

        done()

    def get_wav_from_video(
        self, source_video_path: str, target_audio_path: str, rate: int = 48000
    ):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_audio_path = try_to_get_absolutely_path(target_audio_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_audio_path)
        make_sure_target_does_not_exist(target_audio_path)

        if type(rate) != int:
            raise (Exception("The rate should be an integer!"))

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -vn -ar {str(rate)} "{target_audio_path}"
        """
        )

        done()

    def replace_old_audio_with_new_wav_file_for_a_video(
        self, source_video_path: str, new_wav_audio_path: str, target_video_path: str
    ):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        new_wav_audio_path = try_to_get_absolutely_path(new_wav_audio_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(new_wav_audio_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -i "{new_wav_audio_path}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{target_video_path}"
        """
        )

        done()

    def delay_audio_in_video(self, source_video_path: str, target_video_path: str, delay: str|float):
        source_video_path = try_to_get_absolutely_path(source_video_path)
        target_video_path = try_to_get_absolutely_path(target_video_path)
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        delay = float(delay) # type: ignore
        delay = str(delay)

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -itsoffset {delay} -i "{source_video_path}" -map 0:v -map 1:a -c copy "{target_video_path}"
        """
        )

        done()

    def increase_audio_volume_in_video(
        self, source_video_path: str, target_video_path: str, times: float | str
    ):
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

        t.run(
            f"""
            ffmpeg -i "{source_video_path}" -vcodec copy -af "volume={times}dB" "{target_video_path}"
        """
        )

        done()

    def fix_corrupt_videos_in_a_folder(self, source_folder: str):
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        if not os.path.isdir(source_folder):
            raise Exception("it needs to be a folder")

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(working_dir, "fixed_" + os.path.basename(source_folder))
        if not os.path.exists(new_folder):
            os.makedirs(new_folder, exist_ok=True)

        filelist = disk.get_files(
            source_folder, type_limiter=[".mp4", ".mkv", ".avi", ".rmvb", ".ts"]
        )

        for file in filelist:
            target_video_path = file.replace(source_folder, new_folder)
            target_dir = get_directory_name(target_video_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            if not os.path.exists(target_video_path):
                try:
                    t.run(
                        f"""
                        ffmpeg -i "{file}" -c copy {target_video_path}
                    """
                    )
                except KeyboardInterrupt:
                    t.kill("ffmpeg")
                    t.run(f'rm "{target_video_path}"')
                    exit()

        done()

    def compress_videos_in_a_folder(
        self,
        source_folder: str,
        fps: int = 29,
        resolution: Tuple[int, int] | None = None,
        preset: str = "veryslow",
    ):
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
        new_folder = add_path(
            working_dir, "compressed_" + os.path.basename(source_folder)
        )
        if not os.path.exists(new_folder):
            os.makedirs(new_folder, exist_ok=True)

        filelist = disk.get_files(
            source_folder, type_limiter=[".mp4", ".mkv", ".avi", ".rmvb", ".ts"]
        )

        for file in filelist:
            target_video_path = file.replace(source_folder, new_folder)
            target_dir = get_directory_name(target_video_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            # make_sure_target_does_not_exist(target_video_path)
            if not os.path.exists(target_video_path):
                try:
                    if resolution:
                        t.run(
                            f"""
                            ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale={resolution[0]}:{resolution[1]} -r {fps} -preset {preset} "{target_video_path}"
                        """
                        )
                    else:
                        t.run(
                            f"""
                            ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale=-2:720 -r {fps} -preset {preset} "{target_video_path}"
                        """
                        )
                except KeyboardInterrupt:
                    t.kill("ffmpeg")
                    t.run(f'rm "{target_video_path}"')
                    exit()
        done()

    def format_videos_in_a_folder(self, source_folder: str):
        source_folder = try_to_get_absolutely_path(source_folder)
        make_sure_source_is_absolute_path(source_folder)

        working_dir = get_directory_name(source_folder)
        new_folder = add_path(
            working_dir, "formated_" + os.path.basename(source_folder)
        )
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        filelist = [
            os.path.join(source_folder, f)
            for f in os.listdir(source_folder)
            if f.endswith(".mp4")
        ]

        for file in filelist:
            basename = os.path.basename(file)
            target_video_path = add_path(new_folder, basename)
            make_sure_target_does_not_exist(target_video_path)

            t.run(
                f"""
                ffmpeg -i "{file}" -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 "{target_video_path}"
            """
            )

        done()

    def removeTopAndBottomOfAVideo(
        self, source_video_path: str, target_video_path: str, cropRatio: float = 0.12
    ):
        make_sure_target_does_not_exist(target_video_path)

        clip = VideoFileClip(source_video_path)
        clip = videoUtils.fix_rotation(clip)
        width = clip.w
        height = clip.h
        cropRatio = 0.12
        cropPixels = int(cropRatio * height)
        clip = clip.crop(x1=0, y1=cropPixels, x2=width, y2=height - cropPixels)
        clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            audio_codec="aac",
            verbose=False,
        )

        done()

    def splitVideoToParts(
        self, source_video_path: str, target_video_folder: str, numOfParts: int
    ):
        if not disk.exists(target_video_folder):
            os.mkdir(target_video_folder)

        clip = VideoFileClip(source_video_path)
        clip = videoUtils.fix_rotation(clip)
        length = clip.duration
        partLength = length / numOfParts

        clips: list[Any] = []
        for i in range(numOfParts):
            clips.append(clip.subclip(i * partLength, (i + 1) * partLength))

        for i, c in enumerate(clips):
            c.write_videofile(
                f"{target_video_folder}/{i}.mp4",
                threads=self._cpu_core_numbers,
                audio_codec="aac",
                verbose=False,
            )

        done()

    def add_background_music_files_into_video(
        self,
        source_file_path: str,
        target_file_path: str,
        musicFiles: List[str],
        preDecreaseDBValueForTheMusic: int = 0,
        howManyDBYouWannaTheMusicToDecreaseWhenYouSpeak: int = 15,
    ):
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
        humanVoice: Any = audioProcessor.pydub.AudioSegment.from_file( #type: ignore
            source_file_path, format="mp4"
        )

        # handle input music
        musicSound: Any = audioProcessor.pydub.AudioSegment.from_file( #type: ignore
            musicFiles[0], format="mp3"
        )
        for musicFile in musicFiles[1:]:
            musicSound += audioProcessor.pydub.AudioSegment.from_file( #type: ignore
                musicFile, format="mp3"
            )

        while len(musicSound) < len(humanVoice): #type: ignore
            musicSound *= 2 #type: ignore

        musicSound = musicSound[: len(humanVoice)] #type: ignore
        musicSound -= preDecreaseDBValueForTheMusic #type: ignore

        # handle the silence
        musicSlices: list[Any] = []

        infoOfTheVoice = (
            audioProcessor.getCompleteTimeRangeForNoSilenceAndSilenceAudioSlice(
                humanVoice
            )
        )

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
        tempMp3FilePath = disk.get_a_temp_file_path(source_file_path)
        finalSound.export(tempMp3FilePath, format="mp3")

        # add all those sound to a video file
        videoclip = VideoFileClip(source_file_path)
        audioclip = AudioFileClip(tempMp3FilePath)

        videoclip.audio = audioclip
        videoclip.write_videofile(
            target_file_path, threads=self._cpu_core_numbers, verbose=False
        )

        done()


class DeepVideo:
    """
    For this one, I'll use deep learning.

    It's based on:
    1. ubuntu core
    2. vosk
    3. ffmpeg
    4. moviepy
    5. librosa
    6. pornstar
    7. speechbrain
    """

    def __init__(self):
        from pathlib import Path

        self.video = Video()

        self._cpu_core_numbers = multiprocessing.cpu_count()

        self.config_folder = Path("~/.auto_everything").expanduser() / Path("video")
        if not os.path.exists(self.config_folder):
            t.run_command(f"mkdir -p {self.config_folder}")

        # download
        zip_file = self.config_folder / Path("vosk-en.zip")
        if not disk.exists(zip_file.as_posix()):
            success = network.download(
                "http://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.3.zip",
                zip_file.as_posix(),
                "30MB",
            )
            if success:
                print("download successfully")
            else:
                print("download error")

        # uncompress
        self.vosk_model_folder = self.config_folder / Path("model")
        if not self.vosk_model_folder.exists():
            disk.uncompress(zip_file.as_posix(), self.vosk_model_folder.as_posix())

        # handle speech brain
        speech_model_data_saving_folder = (
            self.config_folder
            / Path("speechbrain")
            / Path("pretrained_models/sepformer-whamr-enhancement")
        )
        if not os.path.exists(speech_model_data_saving_folder):
            t.run_command(f"mkdir -p {speech_model_data_saving_folder}")
        self.speechbrain_sepformer_voice_enhancement_model = separator.from_hparams( #type: ignore
            source="speechbrain/sepformer-whamr-enhancement",
            savedir=speech_model_data_saving_folder,
        )

    '''
    def remove_noise_from_video(self):
        pass
        """
        # Experiment for noise removing
        # What needs to be done is: 1. increase the sample rate. 2. make it work on left-and-right-channel audio
        video = Video()
        deepVideo = DeepVideo()

        input_video_path = "/Users/yingshaoxo/Movies/Videos/good/1.mkv"
        temp_wav_path = "/Users/yingshaoxo/Movies/Videos/good/1_temp.wav"
        final_wav_path = "/Users/yingshaoxo/Movies/Videos/good/1_final.wav"
        output_video_path = "/Users/yingshaoxo/Movies/Videos/good/done.mkv"
        video.get_wav_from_video(input_video_path, temp_wav_path)
        enhanced_speech = (
            deepVideo.speechbrain_sepformer_voice_enhancement_model.separate_file(
                path=temp_wav_path
            )
        )
        enhanced_speech = enhanced_speech[:, :].detach().cpu().squeeze()
        torchaudio.save(final_wav_path, enhanced_speech, 8000)  # type: ignore
        video.replace_old_audio_with_new_wav_file_for_a_video(input_video_path, final_wav_path, output_video_path)
        """
    '''

    def __time_interval_filter(
        self,
        data: Any,
        minimum_interval_time_in_seconds: float = 0.0,
        video_length: float | None = None,
    ):
        temp_data: list[Any] = []
        length = len(data)
        for index, item in enumerate(data):
            start = item["start"]
            end = item["end"]
            start = start - minimum_interval_time_in_seconds
            end = end + minimum_interval_time_in_seconds
            if index == 0:
                start = item["start"] - minimum_interval_time_in_seconds
                if start < 0:
                    start = 0.0
            if index == length - 1:
                end = item["end"]
            temp_data.append([start, end])
        parts: list[Any] = []
        index = 0
        length = len(temp_data)
        if length >= 2:
            while index <= length - 1:
                first_start = temp_data[index][0]
                first_end = temp_data[index][1]
                if index == 0:
                    if first_start > 0:
                        parts.append([0.0, first_start, "silence"])
                if index == length - 1:
                    parts.append([first_start, first_end, "voice"])
                    if video_length != None:
                        if first_end < video_length:
                            parts.append([first_end, video_length, "silence"])
                    break
                next_index = index + 1
                second_start = temp_data[next_index][0]
                second_end = temp_data[next_index][1]
                if first_end <= second_start:
                    parts.append([first_start, first_end, "voice"])
                    if first_end < second_start:
                        parts.append([first_end, second_start, "silence"])
                elif first_end > second_end:
                    first_end = second_start
                    parts.append([first_start, first_end, "voice"])
                index += 1
            return parts
        else:
            return parts

    def __get_raw_data_from_video(self, path: str):
        from vosk import Model, KaldiRecognizer

        assert os.path.exists(path), f"source video file {path} does not exist!"

        # SetLogLevel(0)
        sample_rate = 48000
        model = Model(self.vosk_model_folder.as_posix())
        rec: Any = KaldiRecognizer(model, sample_rate)

        process = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "quiet",
                "-i",
                path,
                "-ar",
                str(sample_rate),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ],
            stdout=subprocess.PIPE,
        )

        data_list: list[Any] = []
        while True:
            if process.stdout is None:
                break
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data): #type: ignore
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
                    start = result["result"][0]["start"]
                    end = result["result"][-1]["end"]
                    text = result["result"]["text"]
                    data_list.append({"start": start, "end": end, "text": text})
            else:
                # print(rec.PartialResult())
                pass
        return data_list

    def __get_data_from_video(
        self,
        path: str,
        minimum_interval_time_in_seconds: float = 0.0,
        video_length: float | None = None,
    ):
        from vosk import Model, KaldiRecognizer

        assert os.path.exists(path), f"source video file {path} does not exist!"

        sample_rate = 16000
        model = Model(self.vosk_model_folder.as_posix())
        rec: Any = KaldiRecognizer(model, sample_rate)

        process = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "quiet",
                "-i",
                path,
                "-ar",
                str(sample_rate),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ],
            stdout=subprocess.PIPE,
        )

        data_list: list[Any] = []
        while True:
            if process.stdout is None:
                break
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if len(result.keys()) >= 2:
                    "{'result': [{'conf': 0.875663, 'end': 4.35, 'start': 4.11, 'word': 'nice'}, {'conf': 1.0, 'end': 5.13, 'start': 4.59, 'word': 'day'}], 'text': 'nice day'}"
                    start = result["result"][0]["start"]
                    end = result["result"][-1]["end"]
                    data_list.append({"start": start, "end": end})
            else:
                # print(rec.PartialResult())
                pass
        return self.__time_interval_filter(
            data_list, minimum_interval_time_in_seconds, video_length
        )

    def remove_silence_parts_from_videos_in_a_folder(
        self,
        source_folder: str,
        target_video_path: str,
        minimum_interval_time_in_seconds: float = 1.0,
        fps: int | None = None,
        resolution: Tuple[int, int] | None = None,
        preset: str = "placebo",
    ):
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

        video_files = [
            video for video in disk.get_files(source_folder, recursive=False)
        ]
        video_files = disk.sort_files_by_time(video_files)
        if resolution != None:
            resolution = (resolution[1], resolution[0])

        parent_clips = [
            videoUtils.fix_rotation(VideoFileClip(video, target_resolution=resolution))
            for video in video_files
        ]
        length = len(video_files)
        remain_clips: list[Any] = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index / length * 100)) + " %...")
            parts = self.__get_data_from_video(
                video_file,
                minimum_interval_time_in_seconds,
                parent_clips[index].duration,
            )
            for part in parts:
                if part[2] == "voice":
                    remain_clips.append(parent_clips[index].subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(remain_clips)
        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            fps=fps,
            preset=preset,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def speed_up_silence_parts_from_videos_in_a_folder(
        self,
        source_folder: str,
        target_video_path: str,
        speed: int = 4,
        minimum_interval_time_in_seconds: float = 1.0,
        fps: int | None = None,
        resolution: Tuple[int, int] | None = None,
        preset: str = "placebo",
    ):
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

        video_files = [
            video for video in disk.get_files(source_folder, recursive=False)
        ]
        video_files = disk.sort_files_by_time(video_files)
        if resolution != None:
            resolution = (resolution[1], resolution[0])
        parent_clips = [
            videoUtils.fix_rotation(VideoFileClip(video, target_resolution=resolution))
            for video in video_files
        ]
        length = len(video_files)
        remain_clips: list[Any] = []
        for index, video_file in enumerate(video_files):
            print("Working on ", str(int(index / length * 100)) + " %...")
            parts = self.__get_data_from_video(
                video_file,
                minimum_interval_time_in_seconds,
                parent_clips[index].duration,
            )
            for part in parts:
                if part[2] == "voice":
                    remain_clips.append(parent_clips[index].subclip(part[0], part[1]))
                elif part[2] == "silence":
                    remain_clips.append(
                        parent_clips[index]
                        .subclip(part[0], part[1])
                        .without_audio()
                        .fx(vfx.speedx, speed)  # type: ignore
                    )

        concat_clip = concatenate_videoclips(remain_clips)
        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            fps=fps,
            preset=preset,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        for parent_clip in parent_clips:
            parent_clip.close()

        done()

    def remove_silence_parts_from_video(
        self,
        source_video_path: str,
        target_video_path: str,
        minimum_interval_time_in_seconds: float = 1.0,
    ):
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
            source_video_path, minimum_interval_time_in_seconds, parent_clip.duration
        )
        clip_list: list[Any] = []
        length = len(parts)
        for index, part in enumerate(parts):
            if part[2] == "voice":
                try:
                    time_duration = part[1] - part[0]
                    print(
                        str(int(index / length * 100)) + "%,",
                        "remain " + str(int(time_duration)) + " seconds",
                    )
                except Exception as e:
                    print(e)
                clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)
        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        parent_clip.close()

        done()

    def speedup_silence_parts_in_video(
        self,
        source_video_path: str,
        target_video_path: str,
        speed: int = 4,
        minimum_interval_time_in_seconds: float = 1.0,
        fps: int | None = None,
        resolution: Tuple[int, int] | None = None,
        preset: str = "placebo",
    ):
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

        if resolution is None:
            parent_clip = VideoFileClip(source_video_path)
        else:
            parent_clip = VideoFileClip(
                source_video_path, target_resolution=(resolution[1], resolution[0])
            )

        parent_clip = videoUtils.fix_rotation(parent_clip)
        parts = self.__get_data_from_video(
            source_video_path, minimum_interval_time_in_seconds, parent_clip.duration
        )
        clip_list: list[Any] = []
        length = len(parts)
        for index, part in enumerate(parts):
            if part[2] == "voice":
                clip_list.append(parent_clip.subclip(part[0], part[1]))
            elif part[2] == "silence":
                try:
                    time_duration = part[1] - part[0]
                    print(
                        str(int(index / length * 100)) + "%,",
                        "speed up " + str(int(time_duration)) + " seconds",
                    )
                except Exception as e:
                    print(e)
                clip_list.append(
                    parent_clip.subclip(part[0], part[1])
                    .without_audio()
                    .fx(vfx.speedx, speed)  # type: ignore
                )

        concat_clip = concatenate_videoclips(clip_list)
        concat_clip.write_videofile(
            target_video_path,
            threads=self._cpu_core_numbers,
            fps=fps,
            preset=preset,
            audio_codec="aac",
            verbose=False,
        )
        concat_clip.close()
        parent_clip.close()

        done()

    def _get_sounds_parts(self, source_audio_path: str, top_db: int):
        y, sr = get_wav_infomation(source_audio_path)
        parts = librosa.effects.split(y, top_db=top_db)  # return samples #type: ignore

        def from_samples_to_seconds(parts: Any):
            parts = librosa.core.samples_to_time(parts, sr=sr)  # return seconds #type: ignore
            new_parts: list[Any] = []
            for part in parts:
                part1 = part[0]
                part2 = part[1]
                new_parts.append([part1, part2])

            return new_parts

        parts[0] = [0, parts[0][1]]
        parts = from_samples_to_seconds(parts)

        return parts[1:]
    
    def improve_the_quality_of_human_voice_inside_of_a_video(
        self, 
        source_video_path: str,
        target_video_path: str, 
        sample_rate: int=48000
        ):
        temp_audio_path = disk.get_a_temp_file_path("temp_audio.wav")
        target_audio_path = disk.get_a_temp_file_path("temp_audio2.wav") 

        convert_video_to_wav(
            source_video_path=source_video_path, 
            target_wav_path=temp_audio_path, 
            sample_rate=sample_rate
        )

        current_working_directory = t.run_command("pwd")
        os.chdir("/tmp")
        if sample_rate == 16000:
            deep_audio.speech_enhancement_with_speechbrain( #type: ignore
                source_audio_path=temp_audio_path,
                target_audio_path=target_audio_path,
                sample_rate=16000
            )
        else:
            deep_audio.speech_enhancement_with_deepFilterNet( #type: ignore
                source_audio_path=temp_audio_path,
                target_audio_path=target_audio_path,
            )
        os.chdir(current_working_directory)

        self.video.replace_old_audio_with_new_wav_file_for_a_video(
            source_video_path=source_video_path, 
            new_wav_audio_path=target_audio_path, 
            target_video_path=target_video_path
        )

        disk.remove_a_file(temp_audio_path)
        disk.remove_a_file(target_audio_path)

        done()

    def blurPornGraphs(self, source_video_path: str, target_video_path: str):
        # useless
        import pornstar  # type: ignore

        def doit(frame: Any):
            if pornstar.store.nsfw_detector.isPorn(frame, 0.9): #type: ignore
                classList, ScoreList, PositionList = pornstar.my_object_detector.detect( #type: ignore
                    frame
                )
                if "person" in classList:
                    frame = pornstar.effect_of_blur(frame, kernel=30) #type: ignore
            return frame

        pornstar.process_video( #type: ignore
            path_of_video=source_video_path,
            effect_function=doit,
            save_to=target_video_path,
        )


def test():
    video = Video()
    deepVideo = DeepVideo()


if __name__ == "__main__":
    pass
