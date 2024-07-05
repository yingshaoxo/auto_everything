from auto_everything.audio_ import Audio
from time import time

audio = Audio()
audio = audio.read_wav_file("/home/yingshaoxo/Downloads/handclap2.wav")

audio.write_wav_file("/home/yingshaoxo/Downloads/smooth_original.wav")

start_time = time()
smooth_1 = audio.copy().smooth_audio()
#for i in range(10):
    #smooth_1 = smooth_1.smooth_audio()
smooth_1.write_wav_file("/home/yingshaoxo/Downloads/smooth_by_volume_gate.wav")
end_time = time()
print("smooth_1", end_time-start_time)
