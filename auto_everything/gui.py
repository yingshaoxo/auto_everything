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


from auto_everything.base import Terminal, Python, OS
t = Terminal()
py = Python()
os_ = OS()


try:
    from PIL import Image
    import pyscreenshot as ImageGrab
except ImportError:
    py.install_package("pyscreenshot")

try:
    import pytesseract
except ImportError:
    t.run("sudo apt install tesseract -y")
    py.install_package("pytesseract")


class Model():
    def __init__(self, __cnn_data_folder):
        self.__cnn_data_folder = __cnn_data_folder
        self.__init_data_structure()

    def __init_data_structure(self):
        if not t.exists(self.__cnn_data_folder):
            os.mkdir(self.__cnn_data_folder)

    def traning(self):
        paths = [os.path.join(self.__cnn_data_folder, filename)
                 for filename in os.listdir(self.__cnn_data_folder)]
        folders = [path for path in paths if os.path.isdir(path)]
        if len(folders) == 0:
            print('You should put image folders into {path}, then you can start traning'.format(
                path=self.__cnn_data_folder))
            exit()

        for folder in folders:
            class_name = os.path.basename(folder)
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(
                os.path.join(folder, f)) and os.path.basename(f).split('.')[-1] in ['png', 'jpg']]
            if len(files) == 0:
                print("Class {c} have no pictures in it".format(c=class_name))
                exit()
            print(files)


class GUI():
    def __init__(self, name="", time_takes_for_one_click=0):
        try:
            import pyautogui as autogui
        except:
            os_.install_package("python3-xlib")
            py.install_package("pyautogui")
            print(
                "failed to load autogui, if you have installed that, run this script without root")
        self.autogui = autogui
        self.autogui.FAILSAFE = False

        self.__data_folder = name + "_data"
        self.__init_data_structure()
        self.__load_data()

        __cnn_data_folder = name + "_cnn_data"
        self.cnn_model = Model(__cnn_data_folder)

        self.__time_takes_for_one_click = time_takes_for_one_click

    def __init_data_structure(self):
        if not t.exists(self.__data_folder):
            os.mkdir(self.__data_folder)

    def __load_data(self):
        paths = [os.path.join(self.__data_folder, filename)
                 for filename in os.listdir(self.__data_folder)]
        files = [path for path in paths if os.path.isfile(path)]
        files = [path for path in paths if os.path.basename(
            path).split('.')[-1] in ["png", "jpg"]]

        self.img_dict = {}
        for file in files:
            obj_name = '.'.join(os.path.basename(file).split('.')[:-1])
            self.img_dict.update({obj_name: file})

    def screen_capture(self, picture_name):
        """
        screenshot with area selecting, based on deepin-screenshot
        """
        target_path = os.path.join(self.__data_folder, picture_name + '.png')
        t.run_command(f'deepin-screenshot -s "{target_path}"')

    def delay(self, seconds):
        time.sleep(seconds)

    def _make_sure_img_dict_exists(self):
        if self.img_dict == {}:
            print('You should put image files (png, jpg) with meaningful name into {path} folder first!'.format(
                path=self.__data_folder))
            exit()

    def __click(self, x, y):
        #self.autogui.moveTo(x, y)
        self.autogui.click(x, y, interval=self.__time_takes_for_one_click)
        self.autogui.click(x, y+1, interval=self.__time_takes_for_one_click)

    def __get_tuple(self, element_name, confidence=0.9):
        return self.autogui.locateCenterOnScreen(element_name, confidence=confidence)

    def hide_mouse(self):
        self.autogui.mouseUp()
        self.delay(1)
        self.autogui.moveTo(0, 0)

    def exists(self, element_name, from_image=None, space_ratio=(0, 0, 1, 1), confidence=0.9):
        """
        element_name: image name (those pictures you put into data folder) ; String

        space_ratio: ratio of area you want to detect (left_top_x, left_top_y, right_bottom_x, right_bottom_y) ; Integer Numbers
        """
        self._make_sure_img_dict_exists()
        print(f"Ask for {element_name}")

        if from_image == None:
            Tuple = self.__get_tuple(
                self.img_dict[element_name], confidence=confidence)
            if Tuple == None:
                return False
            else:
                return True

    def get_center_xy(self, element_name):
        """
        element_name: image name (those pictures you put into data folder) ; String
        """
        self._make_sure_img_dict_exists()

        Tuple = self.__get_tuple(self.img_dict[element_name])
        if Tuple != None:
            x, y = Tuple
        else:
            x, y = 0, 0
        return x, y

    def click(self, element_name):
        self._make_sure_img_dict_exists()
        print(f"Try to click {element_name}")

        Tuple = self.__get_tuple(self.img_dict[element_name])
        if Tuple != None:
            x, y = Tuple
            self.__click(x, y)

    def click_after_exists(self, element_name, space_ratio=(0, 0, 1, 1)):
        """
        element_name: image name (those pictures you put into data folder) ; String

        space_ratio: ratio of area you want to detect (left_top_x, left_top_y, right_bottom_x, right_bottom_y) ; Integer Numbers
        """
        self._make_sure_img_dict_exists()

        while True:
            Tuple = self.__get_tuple(self.img_dict[element_name])
            if Tuple != None:
                x, y = Tuple
                self.__click(x, y)
                break
            time.sleep(1)

    def find_text(self, target_text):
        """
        will return a list of center points

        a point: (x, y)
        """
        result = pytesseract.image_to_data(
            ImageGrab.grab(), output_type='dict')
        target_index = []
        for index, text in enumerate(result['text']):
            if target_text in text:
                target_index.append(index)
        return_list = []
        if (len(target_index) != 0):
            for t_index in target_index:
                list_ = ['top', 'left', 'width', 'height']
                my_dict = {}
                for attribute in list_:
                    value = result[attribute][t_index]
                    my_dict.update({attribute: value})
                x = my_dict['left'] + my_dict['width']/2
                y = my_dict['top'] + my_dict['height']/2
                return_list.append((x, y))
        if (len(return_list) != 0):
            return return_list
        else:
            return None


class Control():
    """
    1. when you hit ctrl+caps , start to write command
    2. / means you want to search text on screen, generate ramdom number for different position, like vimum
    """

    def __init__(self):
        pass


if __name__ == "__main__":
    pass
