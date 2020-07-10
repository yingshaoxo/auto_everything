from typing import List
from pathlib import Path
import os
import re
import json

from auto_everything.base import Terminal
t = Terminal(debug=True)


class Common():
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


class Disk():
    """
    Some useful functions to handle your disk
    """

    def __init__(self):
        pass

    def exists(self, path: str) -> bool:
        """
        Check if a file or folder exist.

        Parameters
        ----------
        path: string
            the file path
        """
        return Path(path).exists()

    def get_files(self, folder: str, recursive: bool = True) -> List[str]:
        """
        Get files recursively under a folder.

        Parameters
        ----------
        folder: string
        recursive: bool
        """
        assert os.path.exists(folder), f"{path} is not exist!"
        if recursive == True:
            files = []
            for root, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    if os.path.isfile(file):
                        files.append(file)
        else:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files

    def sort_files_by_time(self, files: List[str], reverse: bool = False):
        files.sort(key=os.path.getmtime, reverse=reverse)
        return files

    def get_file_size(self, path: str, level: str = "B") -> int:
        """
        Get file size in the unit of  B, KB, MB.

        Parameters
        ----------
        path: string
            the file path
        level: string
            B, KB, or MB
        """
        file = Path(path)
        assert file.exists(), f"{path} is not exist!"
        bytes = file.stat().st_size
        if (level == "B"):
            return int('{:,.0f}'.format(bytes))
        elif (level == "KB"):
            return int('{:,.0f}'.format(bytes/float(1 << 10)))
        elif (level == "MB"):
            return int('{:,.0f}'.format(bytes/float(1 << 20)))

    def uncompress(self, path: str, folder: str = None) -> bool:
        """
        uncompress a file.

        Parameters
        ----------
        path: string
            the compressed file path
        folder: string
            where you want to put the uncompressed files into
        """
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
                t.run(f"tar zxfv '{path}' '{folder}' --strip-components=1")
            if len(os.listdir(folder)):
                return True
            else:
                return False
        except Exception as e:
            raise e


class Store():
    """
    A key-value store.
    """

    def __init__(self, store_name: str, save_to_folder: str = None):
        self._common = Common()

        if save_to_folder is None or not os.path.exists(save_to_folder):
            self._store_folder = self._common._create_a_sub_config_folder_for_auto_everything("store")
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
        self._sql_conn.create_function("REGEXP", 2, regular_expression)  # 2 here means two parameters. REGEXP is a fixed value

        self._sql_cursor = self._sql_conn.cursor()
        self._sql_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._store_name}
                    (key TEXT, value TEXT)''')

    def __pre_process_key(self, key):
        key = str(key)
        return key

    def __pre_process_value(self, value):
        if not isinstance(value, str):
            try:
                value = json.dumps(value)
            except Exception as e:
                print(e)
                raise Exception(f"The value you gave me is not a json object: {str(value)}")
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
        for row in self._sql_cursor.execute(f'SELECT * FROM {self._store_name} ORDER BY key'):
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

        results = self._sql_cursor.execute(f'SELECT EXISTS(SELECT 1 FROM {self._store_name} WHERE key="{key}" LIMIT 1)')
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

        self._sql_cursor.execute(f'SELECT * FROM {self._store_name} WHERE key=?', (key,))
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
            self._sql_cursor.execute(f'UPDATE {self._store_name} SET value=? WHERE key=?', (value, key))
        else:
            command = f''' INSERT INTO {self._store_name} VALUES(?,?) '''
            self._sql_cursor.execute(command, (key, value))
        self._sql_conn.commit()

    def reset(self):
        """
        empty the store
        """
        self._sql_cursor.execute(f'DELETE FROM {self._store_name}')
        self._sql_conn.commit()


if __name__ == "__main__":
    """
    from pprint import pprint
    disk = Disk()
    files = disk.get_files(os.path.abspath(".."))
    files = disk.sort_files_by_time(files)
    pprint(files)
    """
    store = Store("test")
    store.set("o", "2")
    print(store.get_items())
    print(store.has_key("o"))
    print(store.get("ok", "alsjdkfla"))
    store.reset()
    print(store.get_items())
