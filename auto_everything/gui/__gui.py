"""
这个gui识别得分三步走

一， training，我们是做机器学习的，图片、训练集啥的我们得准备好

二，predict，从用户给的图片中得到 object box or center point

三，应用，这个时候才涉及到操作键鼠


1.init_data_structure

2.label_img

3.start_training

4.object_detection(img_name)

5.click(x, y)
"""
import os
import time


# This is for using my parent package
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from base import Terminal, Python
t = Terminal()
py = Python()

sys.path.pop(0)


class Model():
    def __init__(self, __cnn_data_folder):
        self.__cnn_data_folder = __cnn_data_folder
        self.__init_data_structure()

    def __init_data_structure(self):
        if not t.exists(self.__cnn_data_folder):
            os.mkdir(self.__cnn_data_folder)

    def traning(self):
        paths = [os.path.join(self.__cnn_data_folder, filename) for filename in os.listdir(self.__cnn_data_folder)]
        folders = [path for path in paths if os.path.isdir(path)]
        if len(folders) == 0:
            print('You should put image folders into {path}, then you can start traning'.format(path=self.__cnn_data_folder))
            exit()

        for folder in folders:
            class_name = os.path.basename(folder)
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and os.path.basename(f).split('.')[-1] in ['png','jpg']]
            if len(files) == 0:
                print("Class {c} have no pictures in it".format(c=class_name))
                exit()
            print(files)


class GUI():
    def __init__(self, name=""):
        try:
            import pyautogui as autogui
        except:
            t.install_package("python3-xlib")
            py.install_package("pyautogui")
        self.autogui = autogui
        self.autogui.FAILSAFE = False

        self.__data_folder = name + "_data"
        self.__init_data_structure()
        self.__load_data()

        __cnn_data_folder = name + "_cnn_data"
        self.cnn_model = Model(__cnn_data_folder)

    def __init_data_structure(self):
        if not t.exists(self.__data_folder):
            os.mkdir(self.__data_folder)

    def __load_data(self):
        paths = [os.path.join(self.__data_folder, filename) for filename in os.listdir(self.__data_folder)]
        files = [path for path in paths if os.path.isfile(path)]
        files = [path for path in paths if os.path.basename(path).split('.')[-1] in ["png", "jpg"]]
        if len(files) == 0:
            print('You should put image files (png, jpg) with meaningful name into {path} first!'.format(path=self.__data_folder))
            exit()

        self.img_dict = {}
        for file in files:
            obj_name = '.'.join(os.path.basename(file).split('.')[:-1])
            self.img_dict.update({obj_name: file})

    def exists(self, element_name, from_image=None, space_ratio=(0, 0, 1, 1)):
        """
        element_name: image name (those pictures you put into data folder) ; String

        space_ratio: ratio of area you want to detect (left_top_x, left_top_y, right_bottom_x, right_bottom_y) ; Integer Numbers
        """
        if from_image == None:
            Tuple = self.autogui.locateCenterOnScreen(self.img_dict[element_name])
            if Tuple == None:
                return False
            else:
                return True

    def click_after_exists(self, element_name, space_ratio=(0, 0, 1, 1)):
        """
        element_name: image name (those pictures you put into data folder) ; String

        space_ratio: ratio of area you want to detect (left_top_x, left_top_y, right_bottom_x, right_bottom_y) ; Integer Numbers
        """
        while True:
            Tuple = self.autogui.locateCenterOnScreen(self.img_dict[element_name])
            if Tuple != None:
                x, y = Tuple
                self.autogui.moveTo(x, y)
                self.autogui.click()
                break
            time.sleep(1)


if __name__ == "__main__":
    gui = GUI()
    while True:
        print(gui.exists("close"))
        time.sleep(1)
