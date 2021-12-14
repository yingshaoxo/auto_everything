from typing import Callable

from auto_everything.base import Terminal

import tensorflow as tf
import numpy as np
import time

t = Terminal(debug=True)


def checkIfAVaribleIsAFunction(function: Callable) -> bool:
    return isinstance(function, Callable)


class AudioHandler:
    def __init__(self, device_index: int, call_back_function: Callable[[np.ndarray, ], None]):
        import pyaudio
        import librosa

        self.pyaudio = pyaudio
        self.librosa = librosa

        self.FORMAT = self.pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.stream = None

        self.device_index = device_index
        self.call_back_function = call_back_function

    def __del__(self):
        self.stream.close()
        self.p.terminate()

    def start(self):
        self.p = self.pyaudio.PyAudio()
        if self.device_index is None:
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      output=False,
                                      stream_callback=self.callback,
                                      frames_per_buffer=self.CHUNK,
                                      )
        else:
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      output=False,
                                      stream_callback=self.callback,
                                      frames_per_buffer=self.CHUNK,
                                      input_device_index=self.device_index,
                                      # print(self.sounddevice.query_devices())
                                      )

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)

        if checkIfAVaribleIsAFunction(self.call_back_function):
            self.call_back_function(numpy_array)

        # data = librosa.amplitude_to_db(numpy_array)
        # value = tf.math.reduce_mean(data)
        # print(value.numpy())

        return None, self.pyaudio.paContinue

    def mainloop(self):
        while self.stream.is_active():
            time.sleep(2.0)


class AudioMonitor:
    def __init__(self):
        try:
            import sounddevice
            import pyaudio
            self.sounddevice = sounddevice
            self.pyaudio = pyaudio
            self.AudioHandler = AudioHandler
        except Exception as e:
            print("python3 -m pip install sounddevice")
            print("python3 -m pip install pyaudio")
            raise e



if __name__ == "__main__":
    audio = AudioHandler()
    audio.start()  # open the the stream
    audio.mainloop()  # main operations with librosa
    audio.stop()
