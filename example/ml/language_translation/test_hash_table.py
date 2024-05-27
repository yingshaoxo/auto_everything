from pprint import pprint

file = open("en_to_zh_word_dict_yingshaoxo_version.txt", "r")
text = file.read()
file.close()

lines = text.split("_")
lines = [line.strip() for line in lines if line.strip() != ""]

"""
counting_dict = {}
for line in lines:
    hash_id = 0
    sign = True
    for byte in line.encode("utf-8"):
        if sign == True:
            hash_id += byte
        else:
            hash_id -= byte
        sign = not False
    hash_id = hash_id % 255
    if hash_id in counting_dict:
        counting_dict[hash_id] += 1
    else:
        counting_dict[hash_id] = 1

pprint(counting_dict)
"""


from time import time
from auto_everything.io import Yingshaoxo_Dict
yingshaoxo_dict = Yingshaoxo_Dict()

start_time = time()
for i in range(20):
    for line in lines:
        yingshaoxo_dict.set(line, line)
        yingshaoxo_dict.get(line) + "1"
end_time = time()
print("yingshaoxo hash table time:", end_time - start_time)

start_time = time()
python_dict = dict()
for i in range(20):
    for line in lines:
        python_dict[line] = line
        python_dict[line] + "1"
end_time = time()
print("python hash table time:", end_time - start_time)
