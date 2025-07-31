import librosa
import tensorflow as tf

from auto_everything.audio import AudioMonitor
from collections import deque
import time

audioMonitor = AudioMonitor()

d = deque([0], maxlen=1)
NotInSilence = False

def checkIfDequeTimeLargerThanCurrentTimeBy(seconds):
    return time.time() - d[0] > seconds

def get_current_time_in_seconds():
    return time.time()

def add_time_to_deque():
    d.append(get_current_time_in_seconds())

if __name__ == "__main__":
    def callBackFunction(data):
        data = librosa.amplitude_to_db(data)
        value = tf.math.reduce_mean(data)
        value = - value.numpy()
        # print(value)
        if (value < 50):
            add_time_to_deque()

    audioHandler1 = audioMonitor.AudioHandler(4, callBackFunction)
    audioHandler1.start()

    audioHandler2 = audioMonitor.AudioHandler(3, callBackFunction)
    audioHandler2.start()

    while True:
        time.sleep(0.1)
        if checkIfDequeTimeLargerThanCurrentTimeBy(1):
            NotInSilence = False
        else:
            NotInSilence = True
        print(NotInSilence)
