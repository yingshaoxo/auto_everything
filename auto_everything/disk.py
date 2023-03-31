from __future__ import annotations
from dataclasses import dataclass
import datetime
import pathlib
import tempfile
from typing import Any, Iterable, List, Tuple
from pathlib import Path
import os
import re
import json
import hashlib
import unicodedata
import string
from io import BytesIO
from fnmatch import fnmatch

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


@dataclass
class _FileInfo:
    """Data Class for a single file returned by get_files()."""
    path: str
    is_folder: bool
    is_file: bool
    folder: str
    name: str
    level: int
    # parent: _FileInfo | None = None # You could try to make a global dict[path, _FilelInfo], then iterate twice to set parent
    children: List[_FileInfo] | None = None


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
            new_path = str(path.as_posix()) #type: ignore
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
    
    def is_directory(self, path: str) -> bool:
        """
        Check if it is a folder.

        Parameters
        ----------
        path: string
            the file path
        """
        return os.path.isdir(path)

    def executable(self, path: str) -> bool:
        return os.access(path, os.X_OK)

    def concatenate_paths(self, *path: str) -> str:
        return os.path.join(*path) # type: ignore
 
    def join_paths(self, *path: str) -> str:
        return self.concatenate_paths(*path)

    def _parse_gitignore_text_to_list(self, gitignore_text: str) -> list[str]:
        ignore_pattern_list = [line for line in gitignore_text.strip().split("\n") if line.strip() != ""]
        new_ignore_pattern_list:list[str] = []
        for pattern in ignore_pattern_list:
            if pattern.startswith("#"):
                continue
            if pattern.endswith("/"):
                new_ignore_pattern_list.append(pattern.removesuffix("/"))
                new_ignore_pattern_list.append(pattern + "*")
            else:
                new_ignore_pattern_list.append(pattern)
        return new_ignore_pattern_list
    
    def _file_match_the_gitignore_rule_list(self, start_folder: str, file_path: str, ignore_pattern_list: list[str]):
        if not start_folder.endswith("/"):
            start_folder = start_folder + "/"
        else:
            start_folder = start_folder

        if file_path.startswith("./"):
            file_path = file_path[2:]
        
        # if file_path.endswith(".ipynb_checkpoints"):
        #     pass
        
        match = False
        for pattern in ignore_pattern_list:
            if fnmatch(file_path.removeprefix(start_folder), pattern.removeprefix("./")):
                match = True
                break
        return match

    def get_files(
        self, 
        folder: str, 
        recursive: bool = True, 
        type_limiter: List[str] | None = None, 
        gitignore_text: str|None = None
    ) -> List[str]:
        """
        Get files recursively under a folder.

        Parameters
        ----------
        folder: string
        recursive: bool
        type_limiter: List[str]
            a list used to do a type filter, like [".mp3", ".epub"]
        gitignore_text: str
            similar to git's .gitignore file, if any file matchs any rule, it won't be inside of the 'return file list'
        """
        folder = self._expand_user(folder)
        assert os.path.exists(folder), f"{folder} is not exist!"
        if recursive == True:
            files:list[str] = []
            for root, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    file:str = self.join_paths(root, filename)
                    if os.path.isfile(file):
                        if type_limiter:
                            p = Path(file)
                            if len(type_limiter) == 0 or (p.suffix in type_limiter):
                                files.append(file)
                        else:
                            files.append(file)

        else:
            if type_limiter:
                files = [
                    os.path.join(folder, f)
                    for f in os.listdir(folder)
                    if len(type_limiter) == 0
                    or
                    (os.path.isfile(os.path.join(folder, f)) and Path(os.path.join(folder, f)).suffix in type_limiter)
                ]
            else:
                files = [
                    os.path.join(folder, f)
                    for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f))
                ]
        
        if gitignore_text != None:
            ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=gitignore_text)

            result_files:list[str] = []
            for file in files:
                if self._file_match_the_gitignore_rule_list(
                    start_folder=folder,
                    file_path=file,
                    ignore_pattern_list=ignore_pattern_list
                ) == False:
                    result_files.append(file)
            
            files = result_files
        
        return files

    def get_folder_and_files(
        self, 
        folder: str, 
        recursive: bool = True, 
        type_limiter: List[str] | None = None,
        gitignore_text: str|None = None
    ) -> Iterable[_FileInfo]:
        """
        Get files recursively under a folder.

        Parameters
        ----------
        folder: string
        recursive: bool
        type_limiter: List[str]
            a list used to do a type filter, like [".mp3", ".epub"]
        gitignore_text: str
            similar to git's .gitignore file, if any file matchs any rule, it won't be inside of the 'return file list'
        """
        folder = self._expand_user(folder)
        assert os.path.exists(folder), f"{folder} is not exist!"

        ignore_pattern_list = []
        if gitignore_text != None:
            ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=gitignore_text)

        for root, dirnames, filenames in os.walk(folder):
            level = root.replace(folder, '').count(os.sep)
            if level == 0:
                level = 1

            for dirname in dirnames:
                abs_folder_path = os.path.join(root, dirname)

                if gitignore_text != None:
                    if self._file_match_the_gitignore_rule_list(
                        start_folder=folder, 
                        file_path=abs_folder_path,
                        ignore_pattern_list=ignore_pattern_list,
                    ):
                        continue
                
                yield _FileInfo(
                    level=level,
                    path=abs_folder_path,
                    is_folder=True,
                    is_file=False,
                    folder=self.get_directory_name(abs_folder_path),
                    name=dirname,
                )

            for filename in filenames:
                abs_folder_path = os.path.join(root, filename)

                if type_limiter != None:
                    should_remain = False
                    if len(type_limiter) != 0:
                        for suffix in type_limiter:
                            if abs_folder_path.endswith(suffix):
                                should_remain = True
                                break
                    else:
                        should_remain = True
                    if should_remain == False:
                        continue
                
                if gitignore_text != None:
                    if self._file_match_the_gitignore_rule_list(
                        start_folder=folder, 
                        file_path=abs_folder_path,
                        ignore_pattern_list=ignore_pattern_list,
                    ):
                        continue

                if os.path.isfile(abs_folder_path):
                    yield _FileInfo(
                    level=level,
                    path=abs_folder_path,
                    is_folder=False,
                    is_file=True,
                    folder=self.get_directory_name(abs_folder_path),
                    name=filename,
                )

            if recursive == False:
                break
    
    def _super_sort_key_function(self, element: str) -> int:
        text = ""
        for char in element:
            if char.isdigit():
                text += char
            else:
                break
        if len(text) == 0:
            return 0
        return int(text[:10])

    def get_folder_and_files_tree(
        self, 
        folder: str, 
        reverse: bool = False,
        type_limiter: List[str] | None = None,
        gitignore_text: str|None = None,
    ) -> _FileInfo:
        """
        Get files recursively under a folder.

        Parameters
        ----------
        folder: string
        type_limiter: List[str]
            a list used to do a type filter, like [".mp3", ".epub"]
        gitignore_text: str
            similar to git's .gitignore file, if any file matchs any rule, it won't be inside of the 'return file list'
        """
        root = _FileInfo(
            path=folder,
            is_folder=True,
            is_file=False,
            folder=self.get_directory_name(folder),
            name=self.get_file_name(folder),
            level=0,
            children=None
        )

        ignore_pattern_list = []
        if gitignore_text != None:
            ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=gitignore_text)

        def dive(node: _FileInfo):
            folder = node.path

            if not os.path.isdir(folder):
                return 

            items = os.listdir(folder)
            if len(items) == 0:
                return 
            
            files_and_folders: list[_FileInfo] = []
            for filename in items:
                file_path = os.path.join(folder, filename)
                if (os.path.isdir(file_path)) or (type_limiter == None) or (Path(file_path).suffix in type_limiter):
                    # save
                    #absolute_file_path = os.path.abspath(file_path)

                    if gitignore_text != None:
                        if self._file_match_the_gitignore_rule_list(
                            start_folder=node.path, 
                            file_path=file_path,
                            ignore_pattern_list=ignore_pattern_list,
                        ):
                            continue
                    
                    new_node = _FileInfo(
                        path=file_path,
                        is_folder=os.path.isdir(file_path),
                        is_file=os.path.isfile(file_path),
                        folder=self.get_directory_name(file_path),
                        name=self.get_file_name(file_path),
                        level=node.level + 1,
                        children=None
                    )
                    dive(node=new_node)
                    files_and_folders.append(
                        new_node
                    )
                else:
                    # drop
                    continue
            files_and_folders.sort(key=lambda node_: self._super_sort_key_function(node_.name), reverse=reverse)
            node.children = files_and_folders
        
        dive(root)
        
        return root

    def sort_files_by_time(self, files: List[str], reverse: bool = False):
        files.sort(key=os.path.getmtime, reverse=reverse)
        return files

    def get_stem_and_suffix_of_a_file(self, path: str) -> Tuple[str, str]:
        p = Path(path)
        return p.stem, p.suffix

    def get_directory_name(self, path: str):
        path = self._expand_user(path)
        return os.path.dirname(path)

    def get_file_name(self, path: str):
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

    def get_the_temp_dir(self):
        return self.temp_dir

    def get_a_temp_file_path(self, filename: str):
        """
        We'll add a hash_string before the filename, so you can use this file path without any worry
        """
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

    def remove_a_file(self, file_path: str):
        file_path = self._expand_user(file_path)
        if self.exists(file_path):
            os.remove(file_path)

    def delete_a_file(self, file_path: str):
        self.remove_a_file(file_path=file_path)

    def convert_bytes_to_bytes_io(self, bytes_data: bytes) -> BytesIO:
        bytes_io = BytesIO()
        bytes_io.write(bytes_data)
        bytes_io.seek(0)
        return bytes_io

    def create_a_folder(self, folder_path: str):
        folder_path = self._expand_user(folder_path)
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        # if not os.path.exists(folder_path):
        #     os.mkdir(folder_path)

    def fake_folder_backup(self, backup_folder: str, backup_saving_file_path: str | None=None) -> list[Any]:
        saving_path = None
        if backup_saving_file_path != None:
            saving_path = backup_saving_file_path
        files = self.get_folder_and_files(folder=backup_folder)
        data_list: list[Any] = []
        for file_or_folder in files:
            data_list.append({
                "path": file_or_folder.path,
                "type": 'folder' if os.path.isdir(file_or_folder.path) else 'file'
            })
        if (saving_path != None):
            with open(saving_path, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_list, indent=4))
            print(f"fake backup is done, it is in: {saving_path}")
        return data_list

    def fake_folder_recover(self, backup_saving_file_path: str):
        if not disk.exists(backup_saving_file_path):
            raise Exception(f"file does not exists: {backup_saving_file_path}")
        with open(backup_saving_file_path, 'r', encoding='utf-8') as f:
            raw_json = f.read()
            json_object = json.loads(raw_json)
        for item in json_object:
            path = item['path']
            type = item['type']
            if type == 'folder':
                os.mkdir(path)
                print(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("")
                print(path)
        print("\nfake recover is done, sir.")


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

        def regular_expression(expr: str, item: Any):
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

    def __pre_process_key(self, key: Any):
        key = str(key)
        return key

    def __pre_process_value(self, value: Any):
        if not isinstance(value, str):
            try:
                value = json.dumps(value)
            except Exception as e:
                print(e)
                raise Exception(
                    f"The value you gave me is not a json object: {str(value)}"
                )
        return value

    def __active_json_value(self, value: Any):
        try:
            value = json.loads(value)
        except Exception as e:
            value = value
        return value

    def get_items(self):
        """
        get all key and value tuple in the store
        """
        rows:list[Any] = []
        for row in self._sql_cursor.execute(
            f"SELECT * FROM {self._store_name} ORDER BY key"
        ):
            rows.append((row[0], self.__active_json_value(row[1])))
        return rows

    def has_key(self, key: str) -> bool:
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

    def get(self, key: str, default_value: Any):
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

    def set(self, key: str, value: Any):
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

    def delete(self, key: str):
        """
        delete a value by using a key

        Parameters
        ----------
        key: string
        """
        key = self.__pre_process_key(key)

        if self.has_key(key):
            self._sql_cursor.execute(
                f"DELETE FROM {self._store_name} WHERE key=?", (key,)
            )

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
    files = disk.get_files(folder=".", type_limiter=[".mp4"])
    # print(disk.get_hash_of_a_path("/home/yingshaoxo/.python_history"))
