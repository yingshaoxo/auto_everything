import json
import os
import time

import io
import hashlib
import base64

from typing import Any


class IO():
    """
    This is for normal IO processing
    """

    def __init__(self):
        self.current_dir: str = os.getcwd()
        self.__log_path: str = os.path.join(self.current_dir, '.log')

    def make_sure_sudo_permission(self):
        """
        exit if you don't have sudo permission
        """
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()

    def read(self, file_path: str, auto_detect_encoding=False) -> str:
        """
        read text from txt file

        Parameters
        ----------
        file_path
            txt file path
        """
        encoding = 'utf-8'

        if (auto_detect_encoding == True):
            import chardet
            rawdata = open(file_path, "rb").read()
            result = chardet.detect(rawdata)
            if (result != None):
                encoding = result['encoding']
            
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding=encoding, errors="ignore") as f:
                result = f.read()
            return result
        else:
            print(f"File '{file_path}' does not exists.")
            return ""

    def write(self, file_path: str, content: str):
        """
        write text into txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        """
        with open(file_path, 'w', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def append(self, file_path: str, content: str):
        """
        append text at the end of a txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        """
        with open(file_path, 'a', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def string_to_hex(self, utf_8_string: str) -> str:
        return utf_8_string.encode("utf-8", errors="ignore").hex()

    def hex_to_string(self, hex_string: str) -> str:
        return bytes.fromhex(hex_string).decode("utf-8", errors="ignore")

    def __make_sure_txt_exist(self, path: str):
        if not os.path.exists(path):
            self.write(path, "")

    def read_settings(self, key: str, defult: str) -> str:
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            data = json.loads(text)
            return data[key]
        except Exception as e:
            print(e)
            return defult

    def write_settings(self, key: str, value: str) -> bool:
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            try:
                data = json.loads(text)
            except Exception as e:
                print(e)
                data: dict[Any, Any] = dict()
            data.update({key: value})
            text = json.dumps(data)
            self.write(settings_path, text)
            return True
        except Exception as e:
            print(e)
            return False

    def empty_settings(self):
        settings_path = os.path.join(self.current_dir, 'settings.ini')
        try:
            self.write(settings_path, "")
            os.remove(settings_path)
        except Exception as e:
            print(e)

    def log(self, text: str):
        text = str(text)
        now = time.asctime(time.localtime(time.time()))
        text = '\n' * 2 + text + '   ' + '({})'.format(now)
        self.append(self.__log_path, text)

    def get_logs(self):
        return self.read(self.__log_path)


class MyIO():
    def string_to_md5(self, text: str):
        result = hashlib.md5(text.encode())
        return result.hexdigest()

    def base64_to_bytesio(self, base64_string: str):
        img_data = base64.b64decode(base64_string)
        return io.BytesIO(img_data)

    def bytesio_to_base64(self, bytes_io: io.BytesIO):
        bytes_io.seek(0)
        return base64.b64encode(bytes_io.getvalue()).decode()

    def hex_to_bytes(self, hex_string: str):
        return bytes.fromhex(hex_string)

    def bytes_to_hex(self, bytes_data: bytes):
        return bytes_data.hex()

