import os
import platform
import time
import numpy as np
import cv2

from auto_everything.base import Terminal
t = Terminal(debug=True)


class CommonGUI():
    def __init__(self, project_name=""):
        if platform == "darwin":
            # OS X
            print("Sorry, the Mac m1,m2,m3,mx... is totally garbage in my eyes. \nIt even does not support VirtualBox and docker auto-start.\nTry to use Linux, for example, Ubuntu, my friend!")
            exit()
        try:
            import pyautogui as pyautogui
        except Exception:
            error = """
To use this module, you have to install pyautogui:
    sudo apt -y install python3-xlib
    sudo pip3 install pyautogui
    sudo apt -y install python3-tk python3-dev
    sudo apt -y install scrot
            """
            raise Exception(error)

        self.pyautogui = pyautogui
        self.pyautogui.FAILSAFE = False

        self._data_folder = project_name + "_data"
        self._init_data_structure()
        self._load_data()

        self._last_check = {
            "name": "yingshaoxo is a super man",
            "x": 0,
            "y": 0,
        }

    def _init_data_structure(self):
        if not t.exists(self._data_folder):
            os.mkdir(self._data_folder)

    def _load_data(self):
        paths = [os.path.join(self._data_folder, filename)
                 for filename in os.listdir(self._data_folder)]
        files = [path for path in paths if os.path.isfile(path)]
        files = [path for path in paths if os.path.basename(
            path).split('.')[-1] in ["png", "jpg"]]

        self.img_dict = {}
        for file in files:
            obj_name = '.'.join(os.path.basename(file).split('.')[:-1])
            self.img_dict.update({obj_name: file})

    def _make_sure_img_dict_exists(self):
        if self.img_dict == {}:
            print(f'You should put image files (png, jpg) with meaningful name into {self._data_folder} folder first!')
            print("You can do this with the function 'capture_screen_manually(picture_name=**)'")
            exit()

    def capture_screen_manually(self, picture_name):
        """
        screenshot with area selecting, based on gnome-screenshot
        """
        target_path = os.path.join(self._data_folder, picture_name + '.png')
        t.run_command(f'gnome-screenshot -a -f "{target_path}"')

    def delay(self, milliseconds):
        """
        delay for milliseconds
        """
        time.sleep(milliseconds / 1000)

    def find_text(self, target_text, from_image=None):
        """
        will return a list of center points

        a point: (x, y)
        """

        try:
            # from PIL import Image
            import pyscreenshot as ImageGrab
        except ImportError:
            error = """
To use this module, you have to install pyscreenshot:
    sudo pip3 install pyscreenshot
            """
            raise Exception(error)

        try:
            import pytesseract
        except ImportError:
            error = """
To use this module, you have to install tesseract:
    sudo apt -y install tesseract
    sudo pip3 -y install pytesseract
            """
            raise Exception(error)
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
                x = my_dict['left'] + my_dict['width'] / 2
                y = my_dict['top'] + my_dict['height'] / 2
                return_list.append((x, y))
        if (len(return_list) != 0):
            return return_list
        else:
            return None


class GUI(CommonGUI):
    """
    A wrapper for pyautogui.
    """

    def __init__(self, project_name="", time_takes_for_one_click=0.2, grayscale=False):
        CommonGUI.__init__(self, project_name=project_name)
        self.__time_takes_for_one_click = time_takes_for_one_click
        self.__grayscale = grayscale

    def __click(self, x, y, game=False):
        self.pyautogui.click(x, y, interval=self.__time_takes_for_one_click)
        if game == True:
            self.pyautogui.click(x, y + 1, interval=self.__time_takes_for_one_click)

    def __get_tuple(self, element_name, confidence=0.9):
        self._make_sure_img_dict_exists()
        element_name = self.img_dict[element_name]
        return self.pyautogui.locateCenterOnScreen(element_name, confidence=confidence, grayscale=self.__grayscale)

    def hide_mouse(self):
        self.pyautogui.mouseUp()
        self.delay(1)
        self.pyautogui.moveTo(0, 0)

    def exists(self, element_name, confidence=0.9):
        """
        Check if an image exists at the screen

        Parameters
        ----------
        element_name: string
            image name (those pictures you put into data folder)
        """
        print(f"Ask for {element_name}")
        Tuple = self.__get_tuple(
            element_name, confidence=confidence,
        )
        if Tuple == None:
            return False
        else:
            self._last_check["name"] = element_name
            self._last_check["x"] = Tuple[0]
            self._last_check["y"] = Tuple[1]
            return True

    def get_center_point_of(self, element_name, confidence=0.9):
        if element_name == None or element_name == self._last_check["name"]:
            x = self._last_check["x"]
            y = self._last_check["y"]
        else:
            Tuple = self.__get_tuple(element_name, confidence=confidence)
            if Tuple != None:
                x, y = Tuple
            else:
                x, y = None, None
        return x, y

    def click(self, element_name=None, game=False):
        """
        click an image at the screen

        Parameters
        ----------
        element_name: string
            image name (those pictures you put into data folder) 
        game: bool
            for games, we click it in a different way
        """
        print(f"Try to click {element_name}")
        if element_name == None or element_name == self._last_check["name"]:
            x = self._last_check["x"]
            y = self._last_check["y"]
            self.__click(x, y, game=game)
        else:
            Tuple = self.__get_tuple(element_name)
            if Tuple != None:
                x, y = Tuple
                self.__click(x, y, game=game)


class Controller():
    """
    1. when you hit ctrl+caps , start to write command
    2. / means you want to search text on screen, generate ramdom number for different position, like vimum
    """

    def __init__(self):
        try:
            import pyautogui as pyautogui
        except Exception:
            error = """
To use this module, you have to install pyautogui:
    sudo apt -y install python3-xlib
    sudo pip3 install pyautogui
    sudo apt -y install python3-tk python3-dev
            """
            raise Exception(error)
        self.pyautogui = pyautogui

    def get_mouse_position(self):
        return self.pyautogui.position()

    def set_mouse_position(self, x, y):
        self.pyautogui.moveTo(x, y)

    def mouse_click(self, x=None, y=None, button='left', interval=0.5, game=False):
        self.pyautogui.click(x=x, y=y, button=button, interval=interval)
        if game == True:
            self.pyautogui.click(x=x + 1, y=y + 1, button=button, interval=interval)

    def write(self, text: str):
        self.pyautogui.write(text)

    def press(self, key: str):
        """
        self.pyautogui.KEYBOARD_KEYS

        or

        ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
         ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
         '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
         'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
         'browserback', 'browserfavorites', 'browserforward', 'browserhome',
         'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
         'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
         'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
         'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
         'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
         'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
         'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
         'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
         'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
         'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
         'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
         'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
         'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
         'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
         'command', 'option', 'optionleft', 'optionright']
        """
        self.pyautogui.press(key)


class AndroidGUI(CommonGUI):
    """
    To interact with scrcpy by x11 and OpenCV.
    """

    def __init__(self, scrcpy_window_name, project_name=""):
        assert "not found" not in t.run_command("scrcpy -v"), """
To use this module, you have to install scrcpy
        """
        from myx11 import MyX11
        self.myx11 = MyX11()
        self.__window_name = scrcpy_window_name

        assert "not found" not in t.run_command("adb devices"), """
To use this module, you have to install adb:
    sudo apt install android-tools-adb
"""

        try:
            from uiautomator import device as d
            self.d = d
        except Exception as e:
            print(e)
            print(
                "I suggest you to use uiautomator to handle your android phone. You can install it by: \nsudo pip3 install uiautomator")

        info_of_android = t.run_command("adb shell dumpsys display")
        for line in info_of_android.split("\n"):
            if "StableDisplayWidth" in line:
                self.__android_width = int(line.split("=")[1].strip())
            if "StableDisplayHeight" in line:
                self.__android_height = int(line.split("=")[1].strip())

        self.__screen_height = None
        self.__screen_width = None

        CommonGUI.__init__(self, project_name=project_name)

    def capture_screen(self):
        """
        Get opencv image.
        """
        width, height, data = self.myx11.capture_screen(self.__window_name)
        data = cv2.cvtColor(np.array(data, np.uint8).reshape([height, width, 3]), cv2.COLOR_BGR2RGB)
        return data

    def find_all(self, element_name, from_image=None, threshold=0.8, visual=False):
        """
        find all images at the screen

        Parameters
        ----------
        element_name: string
            name for the sub image
        from_image: opencv image
        """
        self._make_sure_img_dict_exists()

        if not isinstance(from_image, np.ndarray):
            from_image = self.capture_screen()
        self.__screen_height = from_image.shape[0]
        self.__screen_width = from_image.shape[1]

        from_image_grayscale = cv2.cvtColor(from_image, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(self.img_dict[element_name], cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(from_image_grayscale, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        result = []
        w, h = template.shape[::-1]
        for pt in zip(*loc[::-1]):
            x, y = (pt[0] + w / 2), (pt[1] + h / 2)
            result.append({"x": x, "y": y})
            if visual:
                cv2.rectangle(from_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if visual:
            return from_image, result
        return result

    def find_one_automatically(self, element_name, from_image=None, threshold=0.5):
        times = 5
        while (times > 0 and 0 < threshold <= 1):
            times -= 1
            print(element_name)
            results = self.find_all(element_name=element_name, from_image=from_image, threshold=threshold)
            if len(results) == 1:
                return results[0]
            elif len(results) > 1:
                threshold += 0.1
            elif len(results) < 1:
                threshold -= 0.1
        return None

    def click(self, point, landscape=True):
        """
        do a click at android screen by using adb

        Parameters
        ----------
        point: {"x": 1920, "y": 1080}
            it's actually the result you get from function find_all().
        """
        assert "x" in point and "y" in point, f"You gave me a wrong point: {str(point)}"
        x = point["x"]
        y = point["y"]
        if landscape:
            x = int(x / self.__screen_width * self.__android_height)
            y = int(y / self.__screen_height * self.__android_width)
        else:
            x = int(x / self.__screen_width * self.__android_width)
            y = int(y / self.__screen_height * self.__android_height)
        t.run(f"adb shell input tap {x} {y}")


if __name__ == "__main__":
    androidGUI = AndroidGUI("pixel")
    while (True):
        data = androidGUI.capture_screen()
        cv2.imshow('frame', data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
