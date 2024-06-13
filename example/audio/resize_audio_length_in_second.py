from auto_everything.audio_ import Audio

audio = Audio()

audio_1 = audio.read_wav_file("/home/yingshaoxo/Downloads/傻逼1.wav").copy()

audio_1.copy().resize(new_audio_length_in_seconds=2, keep_pitch=True).save_to_file("/home/yingshaoxo/Downloads/傻逼_2times.wav")
audio_1.copy().resize(0.5, keep_pitch=True).save_to_file("/home/yingshaoxo/Downloads/傻逼_0.5times.wav")
