from pprint import pprint
from auto_everything.io import IO
io_ = IO()

text = io_.read("./font_8x16.c") # this file is in linux 5.1.1 kernel source code: /lib/fonts/
text = text.split("""
#include <linux/font.h>
#include <linux/module.h>

#define FONTDATAMAX 4096

static const unsigned char fontdata_8x16[FONTDATAMAX] = {
""")[1].split("""
};


const struct font_desc font_vga_8x16 = {
	.idx	= VGA8x16_IDX,
	.name	= "VGA8x16",
	.width	= 8,
	.height	= 16,
""")[0].strip()

raw_character_list = text.split("\n\n")

final_text = ""
for one in raw_character_list:
    one = one.strip()
    splits = one.split("\n")
    head_line = splits[0]
    other_lines = splits[1:]
    symbol = head_line.split("'")[1]
    if symbol == "":
        # it is "'"
        symbol = "'"
    points = ""
    for line in other_lines:
        points += line.split("/* ")[1].split(" */")[0] + "\n"
    points = points.strip()
    final_text += symbol + "\n" + points + "\n\n"

final_text = final_text.strip()
print(final_text)

python_template = "font_data_8x16 = '''\n" + final_text + "\n'''\n"
python_template += """
font_data_8x16 = font_data_8x16.strip()

def get_ascii_8_times_16_font_dict():
    dict_ = {}
    parts = font_data_8x16.split("\\n\\n")
    for part in parts:
        splits = part.split("\\n")
        symbol = splits[0]
        points = []
        for line in splits[1:]:
            points.append([int(one) for one in list(line)])
        dict_[symbol] = points
    return dict_
""".strip()

io_.write("./font.py", python_template)
