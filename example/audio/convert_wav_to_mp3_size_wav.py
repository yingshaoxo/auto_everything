from auto_everything.audio_ import Audio

audio = Audio()

audio = audio.read_wav_file("/home/yingshaoxo/Downloads/song.wav")
audio = audio.get_simplified_audio()

audio.write_wav_file("/home/yingshaoxo/Downloads/song_small.wav")
audio.save_to_file("/home/yingshaoxo/Downloads/song_small.wav.txt")

print("You should get a 3.3MB wav file, but if you convert the output wav file to mp3, it could be smaller, for example, 200KB for a song.")

