from auto_everything.audio_ import Audio

audio = Audio()

audio = audio.read_wav_file("/home/yingshaoxo/Downloads/song.wav")
audio = audio.get_simplified_audio()

audio.write_wav_file("/home/yingshaoxo/Downloads/song_small.wav")
audio.save_to_file("/home/yingshaoxo/Downloads/song_small.wav.txt")

