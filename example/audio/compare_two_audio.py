from auto_everything.audio_ import Audio
from auto_everything.string_ import String

audio = Audio()
string = String()

audio_1 = audio.read_wav_file("/home/yingshaoxo/Downloads/傻逼1.wav").copy()
audio_2 = audio.read_wav_file("/home/yingshaoxo/Downloads/傻逼2.wav").copy()
audio_3 = audio.read_wav_file("/home/yingshaoxo/Downloads/傻叉1.wav").copy()
audio_4 = audio.read_wav_file("/home/yingshaoxo/Downloads/还行1.wav").copy()

audio_1_hash = audio_1.to_hash()
audio_2_hash = audio_2.to_hash()
audio_3_hash = audio_3.to_hash()
audio_4_hash = audio_4.to_hash()

print("high", string.get_similarity_score_of_two_sentence_by_position_match(audio_1_hash, audio_2_hash))
print("little high", string.get_similarity_score_of_two_sentence_by_position_match(audio_1_hash, audio_3_hash))
print()
print("low", string.get_similarity_score_of_two_sentence_by_position_match(audio_1_hash, audio_4_hash))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(audio_2_hash, audio_4_hash))

"""
You have to make sure two audio has same length
"""
