from auto_everything.image import Image
from auto_everything.string_ import String
from time import time as now

string = String()
image = Image()

height, width = 100, 100
image_1 = image.read_image_from_file("/home/yingshaoxo/Downloads/water.png").copy()
image_1 = image_1.resize(height, width)
image_2 = image.read_image_from_file("/home/yingshaoxo/Downloads/freedom.png").copy()
image_2 = image_2.resize(height, width)
image_3 = image.read_image_from_file("/home/yingshaoxo/Downloads/hero.png").copy()
image_3 = image_3.resize(height, width)
image_4 = image.read_image_from_file("/home/yingshaoxo/Downloads/hero3_hqx3.png").copy()
image_4 = image_4.resize(height, width)

start = now()
image1_hash = image_1.to_hash()
image2_hash = image_2.to_hash()
image3_hash = image_3.to_hash()
image4_hash = image_4.to_hash()
end = now()
print("time use:", end-start)
print()

print("low", string.get_similarity_score_of_two_sentence_by_position_match(image1_hash, image2_hash))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(image1_hash, image3_hash))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(image2_hash, image3_hash))
print("high", string.get_similarity_score_of_two_sentence_by_position_match(image4_hash, image3_hash))

