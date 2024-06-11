from auto_everything.audio_ import Audio
from time import time

audio = Audio()
audio = audio.read_wav_file("/home/yingshaoxo/Downloads/handclap2.wav")

start_time = time()
simplifyed_1 = audio.copy().get_simplified_audio(accurate_mode=False)
simplifyed_1 = simplifyed_1.copy().reduce_noise_by_subtraction(use_global_value=True)
simplifyed_1.write_wav_file("/home/yingshaoxo/Downloads/simplifyed_1.wav")
simplifyed_1.save_to_file("/home/yingshaoxo/Downloads/simplifyed_1.wav.txt")
end_time = time()
print("simplified1", end_time-start_time)

start_time = time()
simplifyed_2 = audio.copy().get_extreme_simplified_audio(max_signal_value=9)
simplifyed_2.write_wav_file("/home/yingshaoxo/Downloads/simplifyed_2.wav")
simplifyed_2.save_to_file("/home/yingshaoxo/Downloads/simplifyed_2.wav.txt")
end_time = time()
print("simplified2", end_time-start_time)

start_time = time()
simplifyed_3 = audio.copy().get_simplified_audio_by_using_balance_sample(sample_rate=8000, max_signal_number=30)
simplifyed_3.write_wav_file("/home/yingshaoxo/Downloads/simplifyed_3.wav")
simplifyed_3.save_to_file("/home/yingshaoxo/Downloads/simplifyed_3.wav.txt")
end_time = time()
print("simplified3", end_time-start_time)

start_time = time()
simplifyed_5 = Audio()
simplifyed_5.read_from_file("/home/yingshaoxo/Downloads/simplifyed_3.wav.txt")
print("export data == import data: ", simplifyed_5.raw_data == simplifyed_3.raw_data)
end_time = time()
print("simplified3 read", end_time-start_time)


