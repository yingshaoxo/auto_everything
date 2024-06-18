from auto_everything.audio_ import Audio
from time import time

audio = Audio()
audio = audio.read_wav_file("/home/yingshaoxo/Downloads/piano.wav")

start_time = time()
a_list = audio.copy().split_audio_by_frequency(6)
for index, temp_audio in enumerate(a_list):
    temp_audio.write_wav_file(f"/home/yingshaoxo/Downloads/split_{index}.wav")
end_time = time()
print("done: ", end_time-start_time)

"""
Maybe you can use this to do MIDI pitch recognition from audio.
"""
