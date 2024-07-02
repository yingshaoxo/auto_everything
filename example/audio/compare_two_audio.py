import os
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

#compare_function = string.get_similarity_score_of_two_sentence_by_position_match
compare_function = string.compare_two_sentences

print("high", compare_function(audio_1_hash, audio_2_hash))
print("little high", compare_function(audio_1_hash, audio_3_hash))
print()
print("low", compare_function(audio_1_hash, audio_4_hash))
print("low", compare_function(audio_2_hash, audio_4_hash))

"""
You have to make sure two audio has same length
"""



reply = input("\nDo more test? (y/n)")
if reply.strip().lower() != "y":
    exit()



base_directory = "/home/yingshaoxo/Downloads/audio_test_data/"
category_list = os.listdir(base_directory)
audio_dict = {}

for category in category_list:
    folder_path = base_directory + category + "/"
    files = [folder_path + one for one in os.listdir(folder_path)]
    hash_list = [audio.read_wav_file(one).copy().to_hash() for one in files]
    audio_dict[category] = hash_list

compare_function = string.get_similarity_score_of_two_sentence_by_position_match
#compare_function = string.compare_two_sentences

category_list.sort(reverse=True)
category_list.remove("music")
category_list = ["music"] + category_list
base_hash = audio_dict[category_list[0]][0]
for category in category_list:
    score = 0
    hash_list = audio_dict[category]
    if category == "music":
        hash_list.remove(base_hash)
    value_list = []
    for a_hash in hash_list:
        value = compare_function(base_hash, a_hash)
        score += value
        value_list.append(value)
    score = score / len(hash_list)
    print(category, int(score*100), "      ", value_list)
