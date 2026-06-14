from auto_everything.audio_ import Audio

audio = Audio()
a_audio = audio.read_wav_file("/home/yingshaoxo/Downloads/audio_test_data/test.wav")

a_audio = a_audio.get_super_simplified_audio(positive_number=20000, negative_number=5000)

a_audio.write_wav_file("/home/yingshaoxo/Downloads/audio_test_data/output.wav")
