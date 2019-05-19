import os
import math


from auto_everything.base import Terminal, Python, IO
t = Terminal(debug=True)
py = Python()
io_ = IO()


# begin
import numpy as np
import librosa

import datetime
import shutil

from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx


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


def make_sure_source_is_absolute_path(path):
    path_list = []
    if isinstance(path, str):
        path_list.append(path)
    else:
        path_list = path

    for p in path_list:
        if p[0] == '/':
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
        if p[0] == '/':
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
                if r == False:
                    print("I can't remove target for you, please check your permission")
                    exit()


def convert_video_to_wav(source_video_path, target_wav_path):
    make_sure_source_is_absolute_path(source_video_path)
    make_sure_target_is_absolute_path(target_wav_path)

    make_sure_target_does_not_exist(target_wav_path)

    t.run(f"""
        ffmpeg -i "{source_video_path}" "{target_wav_path}"
    """)

    return target_wav_path


def get_wav_infomation(wav_path):
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
        pass

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
                            [ parts[index-1][1], 
                              parts[index-1][1] + time_gaps 
                            ]
                        )
                        new_parts.append(
                            [ part[0] - time_gaps, 
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

        """
        print()
        print(new_parts)
        print()
        print(all_silence)
        print(new_parts[-1][1])
        print()
        print("the compression ratio: ", all_silence/new_parts[-1][1])
        """
        ratio = all_silence/new_parts[-1][1]
        return ratio
        """
        import matplotlib.pyplot as plt
        import pandas as pd
        data = pd.DataFrame(new_parts)
        print(data)
        data.plot()
        plt.show()
        """

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
        # ffmpeg_command = f'ffmpeg -i "{self._video_file_path}" -ss {time_start} -to {time_end} -async 1 -threads 8 "{target_file_path}"'

        '''
        try:
            clip = VideoFileClip(source_video_path).subclip(time_start, time_end)
            clip.write_videofile(target_video_path)
            clip.close()
            del clip
        except Exception as e:
            print(e)
            print("error at split_video_by_time_part")
            print(time_start)
            print(time_end)
            exit()
        '''

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

    def link_videos(self, source_video_path_list, target_video_path, method=1):
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
        make_sure_source_is_absolute_path(source_video_path_list)
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
            clip_list = [VideoFileClip(clip) for clip in source_video_path_list]
            final_clip = concatenate_videoclips(clip_list)
            final_clip.write_videofile(target_video_path)

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

        if (sort_by_time == False):
            filelist = list(sorted(filelist))
        else:
            filelist.sort(key=lambda x: os.path.getmtime(x))

        self.link_videos(source_video_path_list=filelist,
                         target_video_path=target_video_path, method=method)

        if sort_by_time == False:
            make_sure_target_does_not_exist(source_folder)

        done()

    def remove_noise_from_video(self, source_video_path, target_video_path, degree=0.21, noise_capture_length=None):
        """
        Just as said, remove noise from video
        """
        degree = str(degree)

        make_sure_source_is_absolute_path(source_video_path)
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

    def remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice, minimum_interval_time_in_seconds=None):
        """
        Parameters
        ----------
        source_video_path: string
        target_video_path: string
        db_for_split_silence_and_voice: int
            normoly, it's `20` or `25`, but for some case if the volume is too small, `30` would be fine
        minimum_interval_time_in_seconds: float
            longer than this value, we will take it as silence and remove it
        """
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, 'audio_for_remove_silence_parts_from_video.wav'))
        temp_video_path = add_path(
            working_dir, 'temp_for_remove_silence_parts_from_video.mp4')

        if minimum_interval_time_in_seconds == None:
            parts = self._get_voice_parts(audio_path, top_db)
        else:
            parts = self._get_voice_parts(
                audio_path, top_db, minimum_interval_time_in_seconds)

        # """
        parent_clip = VideoFileClip(source_video_path)
        clip_list = []
        length = len(parts)
        for index, part in enumerate(parts):
            print(str(int(index/length*100))+"%,", part)
            clip_list.append(parent_clip.subclip(part[0], part[1]))

        concat_clip = concatenate_videoclips(clip_list)

        concat_clip.write_videofile(target_video_path)
        concat_clip.close()
        del concat_clip
        # """

        """
        target_folder = add_path(working_dir, "splitted_videos")
        self._split_video_to_parts_by_time_intervals(
            source_video_path, target_folder, parts)

        self.combine_all_mp4_in_a_folder(
            target_folder, target_video_path, sort_by_time=False)
        # self.remove_noise_from_video(source_video_path=temp_video_path, target_video_path=target_video_path)
        """

        make_sure_target_does_not_exist(audio_path)
        make_sure_target_does_not_exist(temp_video_path)

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
        source_video_path = os.path.abspath(source_video_path)
        target_video_path = os.path.abspath(target_video_path)

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, 'audio_for_humanly_remove_silence_parts_from_video.wav'))

        temp_video_path = add_path(
            working_dir, 'temp_for_humanly_remove_silence_parts_from_video.mp4')

        try:
            parts = self._get_voice_parts(
                source_audio_path=audio_path, top_db=db_for_split_silence_and_voice)
            ratio = int(self._evaluate_voice_parts(parts) * 100)
        except Exception as e:
            print(e)
            print()
            print(
                "You probably gave me a wroung db value, try to make it smaller and try it again")
            exit()

        make_sure_target_does_not_exist(temp_video_path)
        make_sure_target_does_not_exist(audio_path)

        answer = input(
            f"Are you happy with the ratio of silence over all: {ratio}% ? (y/n)")
        if answer.strip() == "y":
            print("ok, let's do it!")

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
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        speed = float(speed)

        video_speed = str(float(1/speed))[:6]

        parts = math.ceil(speed/2)
        value_of_each_part = str(speed ** (1/parts))[:6]
        audio_speed = ",".join([f"atempo={value_of_each_part}" for i in range(parts)])

        t.run(f"""
            ffmpeg -i "{source_video_path}" -filter_complex "[0:v]setpts={video_speed}*PTS[v];[0:a]{audio_speed}[a]" -map "[v]" -map "[a]" "{target_video_path}"
        """)

        """
        clip = VideoFileClip(source_video_path).fx(
            vfx.speedx, speed)  # double the speed
        clip.write_videofile(target_video_path)
        """

        done()

    def _speedup_video_with_moviepy(self, source_video_path, target_video_path, speed=4):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        clip = VideoFileClip(source_video_path).without_audio().fx(
            vfx.speedx, speed)
        clip.write_videofile(target_video_path)

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
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(
            working_dir, 'audio_for_speedup_silence_parts_in_video.wav'))
        temp_video_path = add_path(
            working_dir, 'temp_for_speedup_silence_parts_in_video.mp4')

        target_folder = add_path(working_dir, "splitted_videos")
        voice_and_silence_parts = self._get_voice_and_silence_parts(
            audio_path, top_db)

        """
        make_sure_target_does_not_exist(target_folder)
        if not t.exists(target_folder):
            os.mkdir(target_folder)

        for index, part in enumerate(voice_and_silence_parts):
            index = (6-len(str(index)))*'0' + str(index)
            if part[0] == 1:  # voice
                temp_target_video_path = add_path(
                    target_folder, str(index)+".mp4")
                self.split_video_by_time_part(
                    source_video_path, temp_target_video_path, part[1])
            else:  # silence
                temp_for_speedup_video_path = add_path(
                    target_folder, 'temp_for_speedup_silence_parts_in_video.mp4')
                make_sure_target_does_not_exist(temp_for_speedup_video_path)
                self.split_video_by_time_part(
                    source_video_path, temp_for_speedup_video_path, part[1])

                temp_target_video_path = add_path(
                    target_folder, str(index)+".mp4")
                self._speedup_video_with_moviepy(temp_for_speedup_video_path,
                                   temp_target_video_path, speed=speed)
                make_sure_target_does_not_exist(temp_for_speedup_video_path)

        make_sure_target_does_not_exist(audio_path)
        self.combine_all_mp4_in_a_folder(
            target_folder, temp_video_path, sort_by_time=False)
        self.remove_noise_from_video(
            source_video_path=temp_video_path, target_video_path=target_video_path)

        make_sure_target_does_not_exist(temp_video_path)
        """

        make_sure_target_does_not_exist(audio_path)
        parent_clip = VideoFileClip(source_video_path)
        clip_list = []
        length = len(voice_and_silence_parts)
        for index, part in enumerate(voice_and_silence_parts):
            print(str(int(index/length*100))+"%,", part)
            if part[0] == 1:  # voice
                clip_list.append(parent_clip.subclip(part[1][0], part[1][1]))
            else:  # silence
                clip_list.append(
                    parent_clip.subclip(part[1][0], part[1][1]).without_audio().fx(
                        vfx.speedx, speed
                    )
                )

        concat_clip = concatenate_videoclips(clip_list)

        concat_clip.write_videofile(target_video_path)
        concat_clip.close()
        del concat_clip

        done()

    def delay_audio_in_video(self, source_video_path, target_video_path, delay):
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
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)
        make_sure_target_does_not_exist(target_video_path)

        times  = float(times)
        times = str(times)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -vcodec copy -af "volume={times}dB" "{target_video_path}"
        """)

        done()

    def compress_videos_in_a_folder(self, source_folder):
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

        for file in filelist:
            basename = os.path.basename(file)
            target_video_path = add_path(new_folder, basename)
            make_sure_target_does_not_exist(target_video_path)

            size, unit = convert_bytes(os.path.getsize(file))
            if unit == "GB":
                if size > 2:
                    t.run(f"""
                        #ffmpeg -i "{file}" "{target_video_path}"
                        ffmpeg -i "{file}" -c copy -c:v libx264 -vf scale=-2:720 "{target_video_path}"
                    """)

        done()

    def format_videos_in_a_folder(self, source_folder):
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


if __name__ == "__main__":
    video = Video()
    # video.humanly_remove_silence_parts_from_video('/home/yingshaoxo/Videos/doing.mp4', '/home/yingshaoxo/Videos/speed.mp4', 5)
    video.speedup_silence_parts_in_video(
        '/home/yingshaoxo/Videos/doing.mp4', '/home/yingshaoxo/Videos/speed.mp4', 20, 3)
