import datetime
import pathlib
import tempfile
from typing import List, Tuple, Union
from pathlib import Path
import os
import re
import json
import hashlib
import unicodedata
import string
from io import BytesIO

from auto_everything.terminal import Terminal

t = Terminal(debug=True)


class Common:
    def __init__(self):
        self._auto_everything_config_folder = os.path.expanduser("~/.auto_everything")
        # print(self._auto_everything_config_folder)
        if not os.path.exists(self._auto_everything_config_folder):
            os.mkdir(self._auto_everything_config_folder)

    def _create_a_sub_config_folder_for_auto_everything(self, module_name: str):
        sub_folder_path = os.path.join(self._auto_everything_config_folder, module_name)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)
        return sub_folder_path


class Disk:
    """
    Some useful functions to handle your disk
    """

    def __init__(self):
        self.temp_dir: str = tempfile.gettempdir()

    def _expand_user(self, path: str | pathlib.PosixPath):
        # print(type(path))
        new_path: str = ""
        if type(path) == pathlib.PosixPath:
            new_path = path.as_posix()  # type: ignore
        else:
            new_path = path  # type: ignore
        if len(new_path) > 0:
            if new_path[0] == "~":
                new_path = os.path.expanduser(new_path)
        return new_path

    def exists(self, path: str) -> bool:
        """
        Check if a file or folder exist.

        Parameters
        ----------
        path: string
            the file path
        """
        path = self._expand_user(path)
        return Path(path).exists()

    def executable(self, path: str) -> bool:
        return os.access(path, os.X_OK)

    def concatenate_paths(self, *path):
        return os.path.join(*path)

    def get_files(
        self, folder: str, recursive: bool = True, type_limiter: List[str] | None = None
    ) -> List[str]:
        """
        Get files recursively under a folder.

        Parameters
        ----------
        folder: string
        recursive: bool
        type_limiter: List[str]
            a list used to do a type filter, like [".mp3", ".epub"]
        """
        folder = self._expand_user(folder)
        assert os.path.exists(folder), f"{folder} is not exist!"
        if recursive == True:
            files = []
            for root, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    if os.path.isfile(file):
                        if type_limiter:
                            p = Path(file)
                            if p.suffix in type_limiter:
                                files.append(file)
                        else:
                            files.append(file)

        else:
            if type_limiter:
                files = [
                    os.path.join(folder, f)
                    for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f))
                    and Path(os.path.join(folder, f)).suffix in type_limiter
                ]
            else:
                files = [
                    os.path.join(folder, f)
                    for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f))
                ]
        return files

    def sort_files_by_time(self, files: List[str], reverse: bool = False):
        files.sort(key=os.path.getmtime, reverse=reverse)
        return files

    def get_stem_and_suffix_of_a_file(self, path: str) -> Tuple[str, str]:
        p = Path(path)
        return p.stem, p.suffix

    def getDirectoryName(self, path: str):
        path = self._expand_user(path)
        return os.path.dirname(path)

    def getFileName(self, path: str):
        return os.path.split(path)[-1]

    def get_hash_of_a_file(self, path: str) -> str:
        """
        calculate the blake2s hash string based on the bytes of a file.

        Parameters
        ----------
        path: string
            the file path
        """
        path = self._expand_user(path)
        with open(path, "rb") as f:
            file_hash = hashlib.blake2s()
            while True:
                data = f.read(8192)
                if not data:
                    break
                file_hash.update(data)
        return file_hash.hexdigest()

    def get_hash_of_a_path(self, path: str) -> str:
        """
        calculate the blake2s hash string based on path name.

        Parameters
        ----------
        path: string
            actually it can be any string
        """
        file_hash = hashlib.blake2s()
        file_hash.update(path.encode(encoding="UTF-8"))
        return file_hash.hexdigest()

    def get_safe_name(self, filename: str, replace_chars: str = " ") -> str:
        """
        get a valid file name by doing a replacement. (English only)

        Parameters
        ----------
        filename: string
            the unsafe filename
        replace_chars: string
            chars in replace_chars will be replaced by '_'.
        """
        valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        whitelist = valid_filename_chars
        char_limit = 255

        # replace spaces
        for r in replace_chars:
            filename = filename.replace(r, "_")

        # keep only valid ascii chars
        cleaned_filename = (
            unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
        )

        # keep only whitelisted chars
        cleaned_filename = "".join(c for c in cleaned_filename if c in whitelist)
        if len(cleaned_filename) > char_limit:
            print(
                "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                    char_limit
                )
            )
        return cleaned_filename[:char_limit]

    def get_file_size(
        self, path: str, level: str = "B", bytes_size: int | None = None
    ) -> int | None:
        """
        Get file size in the unit of  B, KB, MB.
        Parameters
        ----------
        path: string
            the file path
        level: string
            B, KB, or MB
        bytes_size: int
            a number represent the file size in bytes level
        """
        if bytes_size is None:
            path = self._expand_user(path)
            file = Path(path)
            assert file.exists(), f"{path} is not exist!"
            bytes_size = file.stat().st_size
        if level == "B":
            return int("{:.0f}".format(bytes_size))
        elif level == "KB":
            return int("{:.0f}".format(bytes_size / float(1 << 10)))
        elif level == "MB":
            return int("{:.0f}".format(bytes_size / float(1 << 20)))

    def uncompress(self, path: str, folder: str) -> bool:
        """
        uncompress a file.

        Parameters
        ----------
        path: string
            the compressed file path
        folder: string
            where you want to put the uncompressed files into
        """
        path = self._expand_user(path)
        folder = self._expand_user(folder)
        assert self.exists(path), f"{path} was not exist"

        t.run(f"rm {folder} -fr")
        t.run(f"mkdir -p {folder}")
        assert self.exists(folder), f"{folder} was not exit"
        try:
            suffix = Path(path).suffix
            if suffix == ".zip":
                t.run(f"unzip '{path}' -d '{folder}'")
                if len(os.listdir(folder)) == 1:
                    t.run(f"cd '{folder}' && cd * && mv * .. -f")
            elif suffix == ".gz":
                t.run(f"tar zxfv '{path}' --directory '{folder}' --strip-components=1")
                if len(os.listdir(folder)) == 0:
                    t.run(f"tar zxfv '{path}' --directory '{folder}'")
            if len(os.listdir(folder)):
                return True
            else:
                return False
        except Exception as e:
            raise e

    def compress(self, paths: List[str], target: str):
        """
        compress a files to a target.

        Parameters
        ----------
        paths: string of list
        target: string
            the compressed output file path
        """
        paths = [self._expand_user(path) for path in paths]
        target = self._expand_user(target)
        t.run(f"rm {target}")
        for i, path in enumerate(paths):
            if not self.exists(path):
                raise Exception(f"{path} is not exist")
            paths[i] = f'"{path}"'
        t.run(f"zip -r -D {target} {' '.join(paths)}")

    def get_a_temp_file_path(self, filename):
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode("utf-8"))
        m.update(filename.encode("utf-8"))
        stem, suffix = self.get_stem_and_suffix_of_a_file(filename)
        tempFilePath = os.path.join(self.temp_dir, m.hexdigest()[:10] + suffix)
        return tempFilePath

    def get_the_temp_dir(self):
        return self.temp_dir

    def getATempFilePath(self, filename):
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode("utf-8"))
        m.update(filename.encode("utf-8"))
        stem, suffix = self.get_stem_and_suffix_of_a_file(filename)
        tempFilePath = os.path.join(self.temp_dir, m.hexdigest()[:10] + suffix)
        return tempFilePath

    def create_a_new_folder_under_home(self, folder_name: str):
        folder_path = self._expand_user(f"~/{folder_name}")
        if not os.path.exists(folder_path):
            # os.mkdir(folder_path)
            t.run_command(f"mkdir -p {folder_path}")
        return folder_path

    def get_bytesio_from_a_file(self, filepath: str) -> BytesIO:
        with open(filepath, "rb") as fh:
            buffer = BytesIO(fh.read())
        return buffer

    def save_bytesio_to_file(self, bytes_io: BytesIO, file_path: str):
        bytes_io.seek(0)
        with open(file_path, "wb") as f:
            f.write(bytes_io.read())

    def removeAFile(self, file_path: str):
        file_path = self._expand_user(file_path)
        if self.exists(file_path):
            os.remove(file_path)

    def convertBytesToBytesIO(self, bytes_data: bytes) -> BytesIO:
        bytes_io = BytesIO()
        bytes_io.write(bytes_data)
        bytes_io.seek(0)
        return bytes_io

    def createAFolder(self, folder_path: str):
        folder_path = self._expand_user(folder_path)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)


class Store:
    """
    A key-value store.
    """

    def __init__(self, store_name: str, save_to_folder: str | None = None):
        self._common = Common()

        if save_to_folder is None or not os.path.exists(save_to_folder):
            self._store_folder = (
                self._common._create_a_sub_config_folder_for_auto_everything("store")
            )
        else:
            self._store_folder = save_to_folder

        self._store_name = store_name.strip()
        self.__initialize_SQL()

    def __initialize_SQL(self):
        import sqlite3 as sqlite3

        self._SQL_DATA_FILE = os.path.join(self._store_folder, f"{self._store_name}.db")
        self._sql_conn = sqlite3.connect(self._SQL_DATA_FILE, check_same_thread=False)

        def regular_expression(expr, item):
            reg = re.compile(expr, flags=re.DOTALL)
            return reg.search(item) is not None

        self._sql_conn.create_function(
            "REGEXP", 2, regular_expression
        )  # 2 here means two parameters. REGEXP is a fixed value

        self._sql_cursor = self._sql_conn.cursor()
        self._sql_cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._store_name}
                    (key TEXT, value TEXT)"""
        )

    def __pre_process_key(self, key):
        key = str(key)
        return key

    def __pre_process_value(self, value):
        if not isinstance(value, str):
            try:
                value = json.dumps(value)
            except Exception as e:
                print(e)
                raise Exception(
                    f"The value you gave me is not a json object: {str(value)}"
                )
        return value

    def __active_json_value(self, value):
        try:
            value = json.loads(value)
        except Exception as e:
            value = value
        return value

    def get_items(self):
        """
        get all key and value tuple in the store
        """
        rows = []
        for row in self._sql_cursor.execute(
            f"SELECT * FROM {self._store_name} ORDER BY key"
        ):
            rows.append((row[0], self.__active_json_value(row[1])))
        return rows

    def has_key(self, key) -> bool:
        """
        check if a key exist in the store

        Parameters
        ----------
        key: string
        """
        key = self.__pre_process_key(key)

        results = self._sql_cursor.execute(
            f'SELECT EXISTS(SELECT 1 FROM {self._store_name} WHERE key="{key}" LIMIT 1)'
        )
        if self._sql_cursor.fetchone()[0] > 0:
            return True
        else:
            return False

    def get(self, key, default_value):
        """
        get a value by using a key

        Parameters
        ----------
        key: string
        default_value: string or an object that jsonable
        """
        key = self.__pre_process_key(key)

        self._sql_cursor.execute(
            f"SELECT * FROM {self._store_name} WHERE key=?", (key,)
        )
        result = self._sql_cursor.fetchone()
        if result:
            return self.__active_json_value(result[1])
        else:
            return default_value

    def set(self, key, value):
        """
        set a value by using a key

        Parameters
        ----------
        key: string
        value: string or an object that jsonable
        """
        key = self.__pre_process_key(key)
        value = self.__pre_process_value(value)

        if self.has_key(key):
            self._sql_cursor.execute(
                f"UPDATE {self._store_name} SET value=? WHERE key=?", (value, key)
            )
        else:
            command = f""" INSERT INTO {self._store_name} VALUES(?,?) """
            self._sql_cursor.execute(command, (key, value))
        self._sql_conn.commit()

    def reset(self):
        """
        empty the store
        """
        self._sql_cursor.execute(f"DELETE FROM {self._store_name}")
        self._sql_conn.commit()


if __name__ == "__main__":
    """
    from pprint import pprint
    disk = Disk()
    files = disk.get_files(os.path.abspath(".."))
    files = disk.sort_files_by_time(files)
    pprint(files)
    """
    """
    store = Store("test")
    store.set("o", "2")
    print(store.get_items())
    print(store.has_key("o"))
    print(store.get("ok", "alsjdkfla"))
    store.reset()
    print(store.get_items())
    """
    disk = Disk()
    # print(disk.get_hash_of_a_path("/home/yingshaoxo/.python_history"))
