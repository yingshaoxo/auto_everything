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

print(audio_1_hash)
print(audio_2_hash)
print(audio_3_hash)
print(audio_4_hash)

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
the_test_audio = base_directory + "test.wav"
category_list = os.listdir(base_directory)
category_list = [one for one in category_list if os.path.isdir(os.path.join(base_directory, one))]
audio_dict = {}

for category in category_list:
    folder_path = base_directory + category + "/"
    files = [folder_path + one for one in os.listdir(folder_path)]
    hash_list = [audio.read_wav_file(one).copy().to_hash() for one in files]
    hash_list = [one for one in hash_list if len(one) > 0]
    if len(hash_list) > 0:
        audio_dict[category] = hash_list

print(audio_dict)
#exit()

#compare_function = string.get_similarity_score_of_two_sentence_by_position_match
#compare_function = string.compare_two_sentences
def compare_function(string1, string2):
    if string1 == string2:
        return 1
    else:
        return 0

category_list.sort(reverse=True)
base_hash = audio.read_wav_file(the_test_audio).to_hash()
print(base_hash)
for category in category_list:
    score = 0
    if category not in audio_dict:
        continue
    hash_list = audio_dict[category]
    value_list = []
    for a_hash in hash_list:
        value = compare_function(base_hash, a_hash)
        score += value
        value_list.append(value)
    score = score / len(hash_list)
    print(category, int(score*100), "      ", value_list)
