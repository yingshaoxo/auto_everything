import os


# This is for using my parent package
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from base import Terminal, Python, IO
t = Terminal()
py = Python()
io_ = IO()

sys.path.pop(0)


# begin
import numpy as np
import librosa

import datetime
import shutil

# we'll use ffmpeg to do the real work
class Video():
    def __init__(self, video_file_path=None):
        if video_file_path:
            self._load_video(video_file_path)

    def _load_video(self, video_file_path):
        self._video_file_path = video_file_path
        self._video_directory = os.path.dirname(self._video_file_path)
        self._video_name = os.path.basename(self._video_file_path)

        self._audio_file_path = self.convert_video_to_wav()
        self._audio_name = os.path.basename(self._audio_file_path)

        self._y, self._sr = librosa.load(self._audio_file_path, sr=None)
        
    def convert_video_to_wav(self, video_file_path=None):
        wav_name = "temp.wav"
        
        if video_file_path == None:
            wav_path = os.path.join(self._video_directory, wav_name)
        else:
            wav_path = os.path.join(os.path.dirname(video_file_path), wav_name)

        if t.exists(wav_path):
            os.remove(wav_path)

        command = f"ffmpeg -i {self._video_file_path} {wav_path}"
        t.run(command, wait=True)
        return wav_path

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

    def _get_voice_parts(self, top_db=None, minimum_interval_time_in_seconds=1.5):
        minimum_interval_samples = librosa.core.time_to_samples(minimum_interval_time_in_seconds, self._sr)

        def ignore_short_noise(parts):
            new_parts = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = (part[0] - parts[index-1][1])
                    if (noise_interval > minimum_interval_samples):
                        new_parts.append([parts[index-1][1], parts[index-1][1] + minimum_interval_samples*0.3])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index-1][1], part[0]])
                        new_parts.append(list(part))
            return np.array(new_parts)

        if top_db == None:
            top_db = np.abs(np.max(self._db_clustering(15)))
        parts = librosa.effects.split(self._y, top_db=top_db) # return samples
        parts = ignore_short_noise(parts)

        #new_y = librosa.effects.remix(self._y, parts) # receive samples
        #target_file_path = os.path.join(self._video_directory, "new_" + self._audio_name)
        #if t.exists(target_file_path):
        #    os.remove(target_file_path)
        #librosa.output.write_wav(target_file_path, new_y, self._sr)

        def from_samples_to_seconds(parts):
            parts = librosa.core.samples_to_time(parts, self._sr) # return seconds
            new_parts = []
            def seconds_to_string_format(num):
                return str(datetime.timedelta(seconds=num))
            for part in parts:
                part1 = seconds_to_string_format(part[0])
                part2 = seconds_to_string_format(part[1])
                new_parts.append([part1, part2])
            return new_parts

        parts = from_samples_to_seconds(parts)
        print(parts)
        return parts

    def _split_it_to_parts_by_time_intervals(self, time_intervals):
        video_parts_dir = os.path.join(self._video_directory, 'video_parts')

        if not t.exists(video_parts_dir):
            os.mkdir(video_parts_dir)

        filelist = [ f for f in os.listdir(video_parts_dir) if f.endswith(".mp4") ]
        for f in filelist:
            os.remove(os.path.join(video_parts_dir, f))

        for index, part in enumerate(time_intervals):
            index = (6-len(str(index)))*'0' + str(index)

            time_start = part[0]
            time_end = part[1]
            target_file_path = os.path.join(video_parts_dir, str(index)+".mp4")
            ffmpeg_command = f'ffmpeg -i "{self._video_file_path}" -ss {time_start} -to {time_end} -async 1 -threads 8 "{target_file_path}"'
            print("\n" + "-------------------" + "\n")
            print(ffmpeg_command)
            print()
            t.run(ffmpeg_command, wait=True)

    def combine_all_mp4_in_a_folder(self, video_parts_dir=None):
        sort_by_time = False

        if video_parts_dir == None:
            video_parts_dir = os.path.join(self._video_directory, 'video_parts')
        else:
            sort_by_time = True

        filelist = [ os.path.join(video_parts_dir, f) for f in os.listdir(video_parts_dir) if f.endswith(".mp4") ]

        if (sort_by_time == False):
            filelist = list(sorted(filelist))
        else:
            filelist.sort(key=lambda x: os.path.getmtime(x))

        my_list_text = ''
        for file_path in filelist:
            my_list_text += "file " + f"'{file_path}'" + '\n'

        the_list_path = os.path.join(video_parts_dir, "temp_list.txt")
        io_.write(the_list_path, my_list_text)

        if sort_by_time == False:
            target_file_path = os.path.join(self._video_directory, "new_" + self._video_name)
        else:
            target_file_path = os.path.join(os.path.join(video_parts_dir, ".."), os.path.basename(video_parts_dir) + ".mp4")
        if t.exists(target_file_path):
            os.remove(target_file_path)

        combine_command = f"ffmpeg -f concat -safe 0 -i {the_list_path} {target_file_path}"
        print(combine_command)
        print("\n")
        t.run(combine_command, wait=True)

        if sort_by_time == False:
            shutil.rmtree(video_parts_dir)

        return target_file_path

        '''
            def remove_noise_from_video(self, video_file_path=None):
                if not video_file_path:
                    self._load_video(video_file_path)

                video_file_path = self._video_file_path
                noise_sample_target_path = os.path.join(os.path.dirname(video_file_path), 'noise_sample.wav')
                no_noise_wav_path = os.path.join(os.path.dirname(video_file_path), "new_" + self._audio_name)
                new_video_path = os.path.join(os.path.dirname(video_file_path), "new_" + self._video_name)
                ffmpeg_command = f"""
        ffmpeg -i "{video_file_path}" -acodec pcm_s16le -ar 128k -vn -ss 00:00:00.0 -t 00:00:00.5 "{noise_sample_target_path}"

        sox "{noise_sample_target_path}" -n noiseprof noise.prof

        sox "{self._audio_file_path}" "{no_noise_wav_path}" noisered noise.prof 0.21

        ffmpeg -i "{video_file_path}" -i "{no_noise_wav_path}" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k "{new_video_path}"
                """
                print(ffmpeg_command)
                t.run(ffmpeg_command, wait=True)
        '''

    def remove_silence_parts_from_video(self, video_file_path=None, db_for_split_silence_and_voice=None, minimum_interval_time_in_seconds=None):
        if video_file_path:
            self._load_video(video_file_path)

        if db_for_split_silence_and_voice == None:
            top_db = np.abs(np.max(self._db_clustering(15)))
        else:
            top_db = db_for_split_silence_and_voice

        if minimum_interval_time_in_seconds == None:
            parts = self._get_voice_parts(top_db)
        else:
            parts = self._get_voice_parts(top_db, minimum_interval_time_in_seconds)

        self._split_it_to_parts_by_time_intervals(parts)

        os.remove(self._audio_file_path)

        return self.combine_all_mp4_in_a_folder()

if __name__ == "__main__":
    video = Video("/home/yingshaoxo/Videos/test.mp4")
    parts = video._get_voice_parts(top_db=30)

    import json
    io_.write("/home/yingshaoxo/Downloads/parts.json", json.dumps(parts))

    #video = Video("/home/yingshaoxo/Videos/doing/hi.mp4")
    #video._check_db()

    #inputs = input("What's the db that splited silence and voice? (for example, 20, hit enter to automatically get that value) ")
    #inputs = inputs.strip()
    #if inputs == "":
    #    video.remove_silence_parts_from_video()
    #else:
    #    video.remove_silence_parts_from_video(db_for_split_silence_and_voice=int(inputs))
