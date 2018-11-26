import os


# This is for using my parent package
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from base import Terminal, Python, IO
t = Terminal(debug=True)
py = Python()
io_ = IO()

sys.path.pop(0)


# begin
import numpy as np
import librosa

import datetime
import shutil


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
    def __init__(self):
        pass

    def _db_clustering(self, parts_num=3):
        import librosa.display as display
        import matplotlib.pyplot as plt
        import matplotlib.style as ms

        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(self._y, sr=self._sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        log_S = librosa.power_to_db(S, ref=np.max)

        from sklearn.cluster import KMeans

        x = log_S
        km = KMeans(n_clusters=parts_num)
        km.fit(x.reshape(-1,1))

        return km.cluster_centers_

    def _check_db(self):
        import librosa.display as display
        import matplotlib.pyplot as plt
        import matplotlib.style as ms

        ms.use('seaborn-muted')

        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(self._y, sr=self._sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        log_S = librosa.power_to_db(S, ref=np.max)

        # Make a new figure
        plt.figure(figsize=(12,4))

        # Display the spectrogram on a mel scale
        # sample rate and hop length parameters are used to render the time axis
        display.specshow(log_S, sr=self._sr, x_axis='time', y_axis='mel')

        # Put a descriptive title on the plot
        plt.title('mel power spectrogram')

        # draw a color bar
        plt.colorbar(format='%+02.0f dB')

        # Make the figure layout compact
        plt.tight_layout()

        # show
        plt.show()

    def _get_voice_parts(self, source_audio_path, top_db=None, minimum_interval_time_in_seconds=1.5):
        y, sr = get_wav_infomation(source_audio_path)
        minimum_interval_samples = librosa.core.time_to_samples(minimum_interval_time_in_seconds, sr)

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
                        new_parts.append([parts[index-1][1], parts[index-1][1] + (part[0]-parts[index-1][1])*0.3])
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

        parts = librosa.effects.split(y, top_db=top_db) # return samples
        parts = ignore_short_noise(parts)

        #new_y = librosa.effects.remix(self._y, parts) # receive samples
        #target_file_path = os.path.join(self._video_directory, "new_" + self._audio_name)
        #if t.exists(target_file_path):
        #    os.remove(target_file_path)
        #librosa.output.write_wav(target_file_path, new_y, self._sr)

        def from_samples_to_seconds(parts):
            parts = librosa.core.samples_to_time(parts, sr) # return seconds
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

        return parts

    def _evaluate_voice_parts(self, parts):
        from dateutil.parser import parse
        new_parts = []
        start_timestamp = 0
        for part in parts:
            part1 = parse(part[0]).timestamp()
            part2 = parse(part[1]).timestamp()
            if (start_timestamp == 0):
                start_timestamp = part1
            new_parts.append([part1 - start_timestamp, part2 - start_timestamp])

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

    def split_video_to_parts_by_time_intervals(self, source_video_path, target_folder, time_intervals):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_folder)

        make_sure_target_does_not_exist(target_folder)
        if not t.exists(target_folder):
            os.mkdir(target_folder)

        for index, part in enumerate(time_intervals):
            index = (6-len(str(index)))*'0' + str(index)

            time_start = part[0]
            time_end = part[1]
            target_video_path = add_path(target_folder, str(index)+".mp4")
            #ffmpeg_command = f'ffmpeg -i "{self._video_file_path}" -ss {time_start} -to {time_end} -async 1 -threads 8 "{target_file_path}"'
            ffmpeg_command = f'ffmpeg -i "{source_video_path}" -ss {time_start} -to {time_end} -threads 8 "{target_video_path}"'
            t.run(ffmpeg_command, wait=True)

        done()

    def link_videos(self, source_video_path_list, target_video_path):
        """
        concatenate videos one by one
        """
        make_sure_source_is_absolute_path(source_video_path_list)
        make_sure_target_is_absolute_path(target_video_path)

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

        done()

    def combine_all_mp4_in_a_folder(self, source_folder, target_video_path, sort_by_time=True):
        filelist = [ os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.endswith(".mp4") ]

        if (sort_by_time == False):
            filelist = list(sorted(filelist))
        else:
            filelist.sort(key=lambda x: os.path.getmtime(x))

        self.link_videos(source_video_path_list=filelist, target_video_path=target_video_path)

        if sort_by_time == False:
            make_sure_target_does_not_exist(source_folder)

        done()

    def remove_noise_from_video(self, source_video_path, target_video_path, noise_capture_length=None):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_target_is_absolute_path(target_video_path)

        if not noise_capture_length:
            noise_capture_length = "1"
        else:
            noise_capture_length = str(noise_capture_length)

        working_dir = get_directory_name(target_video_path)

        audio_path = convert_video_to_wav(source_video_path, add_path(working_dir, 'audio.wav'))
        noise_sample_wav_path = add_path(working_dir, 'noise_sample_wav.wav')
        noise_prof_path = add_path(working_dir, 'noise_prof.prof')
        no_noise_wav_path = add_path(working_dir, "no_noise_wav.wav")
        loudnorm_wav_path = add_path(working_dir, "loudnorm_wav.wav")

        make_sure_target_does_not_exist(target_video_path)
        make_sure_target_does_not_exist([noise_sample_wav_path, noise_prof_path, no_noise_wav_path, loudnorm_wav_path])

        t.run(f"""
            ffmpeg -i "{source_video_path}" -acodec pcm_s16le -ar 128k -vn -ss 00:00:00.0 -t 00:00:0{noise_capture_length}.0 "{noise_sample_wav_path}"
        """)

        t.run(f"""
            sox "{noise_sample_wav_path}" -n noiseprof "{noise_prof_path}"
        """)

        t.run(f"""
            sox "{audio_path}" "{no_noise_wav_path}" noisered "{noise_prof_path}" 0.21
        """)

        t.run(f"""
            ffmpeg -i "{no_noise_wav_path}" -af loudnorm=I=-23:LRA=1 -ar 48000 "{loudnorm_wav_path}"
        """)

        t.run(f"""
            ffmpeg -i "{source_video_path}" -i "{loudnorm_wav_path}" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k "{target_video_path}"
        """)

        make_sure_target_does_not_exist([audio_path, noise_sample_wav_path, noise_prof_path, no_noise_wav_path, loudnorm_wav_path])

        done()

    def remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice, minimum_interval_time_in_seconds=None):
        make_sure_source_is_absolute_path(source_video_path)
        make_sure_source_is_absolute_path(target_video_path)

        if db_for_split_silence_and_voice == None:
            top_db = np.abs(np.max(self._db_clustering(15)))
        else:
            top_db = db_for_split_silence_and_voice

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(working_dir, 'audio.wav'))

        if minimum_interval_time_in_seconds == None:
            parts = self._get_voice_parts(audio_path, top_db)
        else:
            parts = self._get_voice_parts(audio_path, top_db, minimum_interval_time_in_seconds)

        target_folder = add_path(working_dir, "splitted_videos")
        self.split_video_to_parts_by_time_intervals(source_video_path, target_folder, parts)

        make_sure_target_does_not_exist(audio_path)

        self.combine_all_mp4_in_a_folder(target_folder, target_video_path, sort_by_time=False)

        done()

    def humanly_remove_silence_parts_from_video(self, source_video_path, target_video_path, db_for_split_silence_and_voice):
        source_video_path = os.path.abspath(source_video_path)
        target_video_path = os.path.abspath(target_video_path)

        working_dir = get_directory_name(target_video_path)
        audio_path = convert_video_to_wav(source_video_path, add_path(working_dir, 'audio.wav'))

        temp_video_path = add_path(working_dir, 'temp_video.mp4')

        try:
            parts = self._get_voice_parts(source_audio_path=audio_path, top_db=db_for_split_silence_and_voice)
            ratio = int(self._evaluate_voice_parts(parts) * 100)
        except Exception as e:
            print(e)
            print()
            print("You probably gave me a wroung db value, try to make it smaller and try it again")
            exit()

        answer = input(f"Are you happy with the ratio of silence over all: {ratio}% ? (y/n)")
        if answer.strip() == "y":
            print("ok, let's do it!")

            self.remove_silence_parts_from_video(source_video_path, temp_video_path, db_for_split_silence_and_voice=db_for_split_silence_and_voice)
            self.remove_noise_from_video(source_video_path=temp_video_path, target_video_path=target_video_path, noise_capture_length=3)

            make_sure_target_does_not_exist(temp_video_path)

            done()
        else:
            print()
            print("you may want to change the db, and try again.")
            exit()

if __name__ == "__main__":
    video = Video()
    #video.link_videos(['/home/yingshaoxo/Videos/clips/money.mp4', '/home/yingshaoxo/Videos/clips/money.mp4'], '/home/yingshaoxo/Videos/hi.mp4')
    #video.combine_all_mp4_in_a_folder("/home/yingshaoxo/Videos/test")
    #video.remove_noise_from_video("/home/yingshaoxo/Videos/demo.mp4", "/home/yingshaoxo/Videos/doing.mp4")
    #video.remove_silence_parts_from_video(source_video_path='/home/yingshaoxo/Videos/demo.mp4', target_video_path='/home/yingshaoxo/Videos/doing.mp4', db_for_split_silence_and_voice=20)
    video.humanly_remove_silence_parts_from_video('/home/yingshaoxo/Videos/demo.mp4', '/home/yingshaoxo/Videos/doing.mp4', db_for_split_silence_and_voice=20)
