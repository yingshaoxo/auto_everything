from auto_everything.audio_ import Audio

audio = Audio()
a_audio = audio.read_wav_file("/home/yingshaoxo/Downloads/audio_test_data/test.wav")

another_audio = a_audio.copy().remove_silence_head_and_tail()
another_audio.write_wav_file("/home/yingshaoxo/Downloads/audio_test_data/output.wav")

