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

# we'll use ffmpeg to do the real work
class Video():
    def __init__(self, video_file_path):
        self.video_file_path = video_file_path
        self.video_directory = os.path.dirname(self.video_file_path)
        self.video_name = os.path.basename(self.video_file_path)

        self.audio_file_path = self.convert_it_to_wav()
        self.audio_name = os.path.basename(self.audio_file_path)

        self.y, self.sr = librosa.load(self.audio_file_path, sr=None)

    def convert_it_to_wav(self):
        wav_path = os.path.join(self.video_directory, "temp.wav")
        if t.exists(wav_path):
            os.remove(wav_path)
        command = f"ffmpeg -i {self.video_file_path} {wav_path}"
        t.run(command, wait=True)
        return wav_path

    def db_clustering(self, parts_num=3):
        import librosa.display as display
        import matplotlib.pyplot as plt
        import matplotlib.style as ms

        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(self.y, sr=self.sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        log_S = librosa.power_to_db(S, ref=np.max)

        from sklearn.cluster import KMeans

        x = log_S
        km = KMeans(n_clusters=parts_num)
        km.fit(x.reshape(-1,1))

        return km.cluster_centers_

    def check_db(self):
        import librosa.display as display
        import matplotlib.pyplot as plt
        import matplotlib.style as ms

        ms.use('seaborn-muted')

        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(self.y, sr=self.sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        log_S = librosa.power_to_db(S, ref=np.max)

        # Make a new figure
        plt.figure(figsize=(12,4))

        # Display the spectrogram on a mel scale
        # sample rate and hop length parameters are used to render the time axis
        display.specshow(log_S, sr=self.sr, x_axis='time', y_axis='mel')

        # Put a descriptive title on the plot
        plt.title('mel power spectrogram')

        # draw a color bar
        plt.colorbar(format='%+02.0f dB')

        # Make the figure layout compact
        plt.tight_layout()

        # show
        plt.show()

    def get_vioce_parts(self, top_db=None, minimum_interval_frames=50000):
        def ignore_short_noise(parts):
            new_parts = []
            for index, part in enumerate(parts):
                if index == 0:
                    new_parts.append(list(part))
                    continue
                else:
                    noise_interval = (part[0] - parts[index-1][1])
                    if (noise_interval > minimum_interval_frames):
                        new_parts.append([parts[index-1][1], parts[index-1][1] + minimum_interval_frames*0.3])
                        new_parts.append(list(part))
                    else:
                        new_parts.append([parts[index-1][1], part[0]])
                        new_parts.append(list(part))
            return np.array(new_parts)

        if top_db == None:
            top_db = np.abs(np.max(self.db_clustering(15)))
        parts = librosa.effects.split(self.y, top_db=top_db)
        parts = ignore_short_noise(parts)

        new_y = librosa.effects.remix(video.y, parts)
        target_file_path = os.path.join(self.video_directory, "new_" + self.audio_name)
        if t.exists(target_file_path):
            os.remove(target_file_path)
        librosa.output.write_wav(target_file_path, new_y, video.sr)

        def from_frames_to_seconds(parts):
            parts = librosa.core.frames_to_time(parts, self.sr)
            parts = parts / 1000
            new_parts = []
            def seconds_to_string_format(num):
                return str(datetime.timedelta(seconds=num))
            for part in parts:
                part1 = seconds_to_string_format(part[0])
                part2 = seconds_to_string_format(part[1])
                new_parts.append([part1, part2])
            return new_parts

        parts = from_frames_to_seconds(parts)
        print(parts)
        return parts

    def split_it_to_parts_by_time_intervals(self, time_intervals):
        video_parts_dir = os.path.join(self.video_directory, 'video_parts')

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
            ffmpeg_command = f'ffmpeg -i "{self.video_file_path}" -ss {time_start} -to {time_end} -async 1 "{target_file_path}"'
            print("\n" + "-------------------" + "\n")
            print(ffmpeg_command)
            print()
            t.run(ffmpeg_command, wait=True)

    def combine_all_mp4_in_a_folder(self):
        video_parts_dir = os.path.join(self.video_directory, 'video_parts')

        filelist = [ f for f in os.listdir(video_parts_dir) if f.endswith(".mp4") ]
        filelist = list(sorted(filelist))
        my_list_text = ''
        for f in filelist:
            file_path = os.path.join(video_parts_dir, f)
            my_list_text += "file " + f"'{file_path}'" + '\n'

        the_list_path = os.path.join(video_parts_dir, "temp_list.txt")
        io_.write(the_list_path, my_list_text)

        target_file_path = os.path.join(self.video_directory, "new_" + self.video_name)
        if t.exists(target_file_path):
            os.remove(target_file_path)

        combine_command = f"ffmpeg -f concat -safe 0 -i {the_list_path} -c copy {target_file_path}"
        print(combine_command)
        print("\n")
        t.run(combine_command, wait=True)

if __name__ == "__main__":
    video = Video("/home/yingshaoxo/Videos/doing/hi.mp4")
    video.check_db()

    inputs = input("What's the db? (for example, 20) ")
    if inputs.strip() == "":
        top_db = np.abs(np.max(video.db_clustering(15)))
        parts = video.get_vioce_parts(top_db)
    else:
        parts = video.get_vioce_parts(int(inputs))

    video.split_it_to_parts_by_time_intervals(parts)
    video.combine_all_mp4_in_a_folder()
