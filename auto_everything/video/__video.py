import os


# This is for using my parent package
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from base import Terminal, Python
t = Terminal()
py = Python()

sys.path.pop(0)


# begin
import numpy as np
import librosa

class Video():
    def __init__(self, video_file_path):
        self.video_file_path = video_file_path
        self.audio_file_path = video_file_path

        self.y, self.sr = librosa.load(self.audio_file_path, sr=None)

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

    def get_silence_parts(self, top_db=None):
        if top_db == None:
            top_db = np.abs(np.max(self.db_clustering()))
        parts = librosa.effects.split(self.y, top_db=top_db)
        print(parts)


if __name__ == "__main__":
    #audio_path = librosa.util.example_audio_file()
    audio_path = '/home/yingshaoxo/Videos/output.wav'

    video = Video(audio_path)
    #video.db_clustering(3)
    video.get_silence_parts(10)
    video.check_db()

