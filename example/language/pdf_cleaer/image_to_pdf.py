import os
from PIL import Image
from fpdf import FPDF

from auto_everything.image_ import Image as Super_Image
super_image = Super_Image()

folder_path = "./output_2/"
a_list = os.listdir(folder_path)

os.system(f"rm -fr {folder_path}_*")
os.system(f"rm -fr {folder_path}*.jpg")

pdf = FPDF()
for img_file in a_list:
    page_width = pdf.w
    page_height = pdf.h

    an_image = super_image.read_image_from_file(folder_path+img_file)
    white_and_black = an_image.copy().to_white_and_black(threshold=200)
    white_and_black.save_image_to_file_path(folder_path+"_"+img_file+".png")

    # size get increased after convert to jpg

    pdf.add_page()
    pdf.image(folder_path+"_"+img_file+".png", x=0, y=0, w=page_width)
pdf.output("output.pdf")
