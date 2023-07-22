from __future__ import annotations
import base64
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
import shutil
import random

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
    
    def join_relative_paths(self, path1: str, path2: str) -> str:
        """
        Join path like: /aa/bb/cc + .././../d.txt
        This function will only care the second relative path
        """
        if path2.startswith("."):
            if path2.startswith("../"):
                return self.join_relative_paths('/'.join(path1.split('/')[:-1]) + "/", path2.replace("../", "", 1))
            elif path2.startswith("./"):
                return self.join_relative_paths(path1, path2.replace("./", "", 1))
            else:
                return self.join_paths(path1, path2)
        else:
            return self.join_paths(path1, path2)
    
    def get_current_working_directory(self) -> str:
        """
        Similar to bash script: `cwd`
        """
        return os.getcwd()

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
    
    def get_absolute_path(self, path: str) -> str:
        return os.path.abspath(path=path)

    def get_stem_and_suffix_of_a_file(self, path: str) -> Tuple[str, str]:
        """
        /hi/you/abc.txt -> ('abc', '.txt')
        """
        p = Path(path)
        return p.stem, p.suffix

    def get_directory_path(self, path: str):
        """
        /hi/you/abc.txt -> /hi/you
        """
        path = self._expand_user(path)
        return os.path.dirname(path)
    
    def get_directory_name(self, path: str):
        """
        /hi/you/abc.txt -> you
        /hi/you -> you
        """
        path = self._expand_user(path)
        if self.exists(path):
            if os.path.isfile(path):
                path = os.path.dirname(path)
        else:
            raise Exception(f"Sorry, I don't know if '{path}' is a folder or file, because folder can also has '.' inside.")
        return os.path.basename(path)

    def get_parent_directory_name(self, path: str):
        """
        /hi/you/abc.txt -> you
        /hi/you -> hi
        """
        path = self._expand_user(path)
        path = os.path.dirname(path)
        return os.path.basename(path)

    def get_file_name(self, path: str):
        """
        /hi/you/abc.txt -> abc.txt
        """
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
        self, path: str | None, level: str = "B", bytes_size: int | None = None
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
            if path != None:
                path = self._expand_user(path)
                file = Path(path)
                assert file.exists(), f"{path} is not exist!"
                bytes_size = file.stat().st_size
            else:
                raise Exception("You should give me a file_path or bytes_size")
        if level == "B":
            return int("{:.0f}".format(bytes_size))
        elif level == "KB":
            return int("{:.0f}".format(bytes_size / float(1 << 10)))
        elif level == "MB":
            return int("{:.0f}".format(bytes_size / float(1 << 20)))

    def compress(self, input_folder_path: str, output_zip_path: str, file_format: str = "zip") -> str:
        """
        compress files to a target.

        Parameters
        ----------
        input_folder_path: string
            the input folder for compressing
        output_zip_path: string
            the compressed output file path, like *.zip
        file_format: string
            “zip”, “tar”, “gztar”, “bztar”, or “xztar”
        """
        input_folder_path = self._expand_user(input_folder_path)
        output_zip_path = self._expand_user(output_zip_path)

        if not self.exists(input_folder_path):
            raise Exception(f"The input_folder_path '{input_folder_path}' should exists.")
        if not self.is_directory(input_folder_path):
            raise Exception(f"The input_folder_path '{input_folder_path}' should be an folder.")
        
        output_folder = self.get_directory_path(output_zip_path)
        self.create_a_folder(folder_path=output_folder)

        pure_output_zip_base_name, suffix = self.get_stem_and_suffix_of_a_file(output_zip_path)
        shutil.make_archive(
            root_dir=input_folder_path,
            base_dir='./',
            base_name=self.join_paths(output_folder, pure_output_zip_base_name),
            format=file_format
        )
        # t.run(f"zip -r -D {target} {' '.join(paths)}")

        return output_zip_path

    def uncompress(self, compressed_file_path: str, extract_folder_path: str, file_format: str = "zip") -> bool:
        """
        uncompress a file.

        Parameters
        ----------
        compressed_file_path: string
            the compressed file path
        extract_folder_path: string
            a folder where you want to put the uncompressed files into
        file_format: string
            “zip”, “tar”, “gztar”, “bztar”, or “xztar”
        """
        try:
            compressed_file_path = self._expand_user(compressed_file_path)
            extract_folder_path = self._expand_user(extract_folder_path)

            if not self.exists(compressed_file_path):
                raise Exception(f"The compressed_file_path '{compressed_file_path}' should exists.")
            if not self.exists(extract_folder_path):
                self.create_a_folder(folder_path=extract_folder_path)

            shutil.unpack_archive(filename=compressed_file_path, extract_dir=extract_folder_path, format=file_format)

            return True
        except Exception as e:
            print(f"error: {e}")
            return False
        # path = self._expand_user(path)
        # folder = self._expand_user(folder)
        # assert self.exists(path), f"{path} was not exist"

        # t.run(f"rm {folder} -fr")
        # t.run(f"mkdir -p {folder}")
        # assert self.exists(folder), f"{folder} was not exit"
        # try:
        #     suffix = Path(path).suffix
        #     if suffix == ".zip":
        #         t.run(f"unzip '{path}' -d '{folder}'")
        #         if len(os.listdir(folder)) == 1:
        #             t.run(f"cd '{folder}' && cd * && mv * .. -f")
        #     elif suffix == ".gz":
        #         t.run(f"tar zxfv '{path}' --directory '{folder}' --strip-components=1")
        #         if len(os.listdir(folder)) == 0:
        #             t.run(f"tar zxfv '{path}' --directory '{folder}'")
        #     if len(os.listdir(folder)):
        #         return True
        #     else:
        #         return False
        # except Exception as e:
        #     raise e

    def get_the_temp_dir(self) -> str:
        """
        Get system level temporary folder. It's normally `/tmp/`
        """
        return self.temp_dir

    def get_a_temp_folder_path(self):
        """
        We'll add a random hash_string after the temp directory, so you can get a path like '/tmp/xxssddf'
        """
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode("utf-8"))
        m.update(''.join(random.choices(string.ascii_uppercase, k=10)).encode("utf-8"))
        temp_folder_path = os.path.join(self.temp_dir, m.hexdigest()[:27])
        return temp_folder_path

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

    def base64_to_bytesio(self, base64_string: str):
        splits = base64_string.split(",")
        if len(splits) == 2:
            base64_string = splits[1]
        img_data = base64.b64decode(base64_string)
        return BytesIO(img_data)

    def bytesio_to_base64(self, bytes_io: BytesIO):
        bytes_io.seek(0)
        return base64.b64encode(bytes_io.getvalue()).decode()

    def bytes_to_base64(self, bytes_data: bytes):
        return base64.b64encode(bytes_data).decode()

    def base64_to_bytes(self, base64_string: str):
        splits = base64_string.split(",")
        if len(splits) == 2:
            base64_string = splits[1]
        img_data = base64.b64decode(base64_string)
        return img_data

    def hex_to_bytes(self, hex_string: str):
        return bytes.fromhex(hex_string)

    def bytes_to_hex(self, bytes_data: bytes):
        return bytes_data.hex()

    def remove_a_file(self, file_path: str):
        file_path = self._expand_user(file_path)
        if self.exists(file_path):
            os.remove(file_path)

    def delete_a_file(self, file_path: str):
        self.remove_a_file(file_path=file_path)

    def move_a_file(self, source_file_path: str, target_file_path: str):
        source_file_path = self._expand_user(source_file_path)
        target_file_path = self._expand_user(target_file_path)
        if source_file_path == target_file_path:
            return
        if self.exists(target_file_path):
            os.remove(target_file_path)
        os.rename(source_file_path, target_file_path)

    def convert_bytes_to_bytesio(self, bytes_data: bytes) -> BytesIO:
        bytes_io = BytesIO()
        bytes_io.write(bytes_data)
        bytes_io.seek(0)
        return bytes_io

    def create_a_folder(self, folder_path: str):
        folder_path = self._expand_user(folder_path)
        Path(folder_path).mkdir(parents=True, exist_ok=True)

    def copy_a_folder(self, source_folder_path: str, target_folder_path: str):
        source_folder_path = self._expand_user(source_folder_path)
        target_folder_path = self._expand_user(target_folder_path)

        if (not self.exists(target_folder_path)):
            self.create_a_folder(target_folder_path)
        else:
            if not self.is_directory(target_folder_path):
                self.delete_a_file(target_folder_path)

        try:
            shutil.copytree(source_folder_path, target_folder_path, dirs_exist_ok=True)
        except OSError as exc: # python >2.5
            try:
                shutil.copy(source_folder_path, target_folder_path)
            except Exception as e:
                print(e)

    def delete_a_folder(self, folder_path: str):
        folder_path = self._expand_user(folder_path)
        if (self.exists(folder_path)):
            shutil.rmtree(path=folder_path)

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

    def read_bytes_from_file(self, file_path: str) -> bytes:
        """
        read bytes from a file

        Parameters
        ----------
        file_path: str
            like `/home/yingshaoxo/file.sql`
        """
        with open(file_path, 'rb') as f:
            result = f.read()
        return result

    def write_bytes_into_file(self, file_path: str, content: bytes):
        """
        write bytes into a file

        Parameters
        ----------
        file_path: str
            target file path
        content: bytes
        """
        with open(file_path, 'wb') as f:
            f.write(content)

    def convert_file_suffix_end_to_lowercase(self, source_folder: str):
        files = list(disk.get_files(source_folder, recursive=True))
        for file in files:
            file = disk.get_absolute_path(file)
            if ("/" in file):
                last_part = file.split("/")[-1]
                if ("." in last_part):
                    end = last_part.split(".")[-1]
                    if file.endswith("." + end):
                        new_file = file[:-len(end)] + end.lower()
                        disk.move_a_file(source_file_path=file, target_file_path=new_file)


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

    def get(self, key: str, default_value: Any = None):
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


class Dart_File_Hard_Encoder_And_Decoder:
    """
    Put a folder into your code as a dart file (yingshaoxo)
    """
    def __init__(self, generated_file_name="built_in_files.dart"):
        from auto_everything.io import IO
        from auto_everything.disk import Disk
        import json
        self._disk = Disk()
        self._io = IO()
        self._json = json

    def _get_content_json_string(self, source_folder: str) -> str: 
        files = self._disk.get_folder_and_files(folder=source_folder, recursive=True)
        object_list = []
        for file in files:
            """
            'is_folder': this.is_folder,
            'relative_path': this.relative_path,
            'base64_content': this.base64_content,
            """
            an_object = {}
            an_object['relative_path'] = file.path
            if file.is_folder:
                an_object['is_folder'] = True
                an_object['base64_content'] = ""
            else:
                an_object['is_folder'] = False
                an_object['base64_content'] = self._disk.bytesio_to_base64(self._disk.get_bytesio_from_a_file(file.path)) 
            object_list.append(an_object)
        return json.dumps(object_list)

    def generate(self, source_folder: str, generated_file_path="lib/built_in_files.dart"):
        template1 = """
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:path/path.dart' as path_;
        """.strip()

        template2 = """
class File_Model {
  bool? is_folder;
  String? relative_path;
  String? base64_content;

  File_Model({this.is_folder, this.relative_path, this.base64_content});

  Map<String, dynamic> to_dict() {
    return {
      'is_folder': this.is_folder,
      'relative_path': this.relative_path,
      'base64_content': this.base64_content,
    };
  }

  File_Model from_dict(Map<String, dynamic>? json) {
    if (json == null) {
      return File_Model();
    }

    this.is_folder = json['is_folder'];
    this.relative_path = json['relative_path'];
    this.base64_content = json['base64_content'];

    return File_Model(
      is_folder: json['is_folder'],
      relative_path: json['relative_path'],
      base64_content: json['base64_content'],
    );
  }
}

Future<Uint8List> decode_base64_string(String content) async {
  return base64Decode(content.replaceAll(RegExp(r'\s'), ''));
}

Future<void> _write_base64_string_to_file(
    String content, String file_path) async {
  Uint8List bytes_data = await decode_base64_string(content);
  await File(file_path).parent.create(recursive: true);
  await File(file_path).writeAsBytes(bytes_data);
}

Future<void> _write_file_object_to_disk(
    File_Model a_file, String parent_folder) async {
  if (a_file.is_folder == null ||
      a_file.relative_path == null ||
      a_file.base64_content == null) {
    return;
  }

  String target_path = path_.join(parent_folder, a_file.relative_path!);

  if (a_file.is_folder == true) {
    if (!Directory(target_path).existsSync()) {
      await Directory(target_path).create(recursive: true);
    }
  } else {
    if (!File(target_path).existsSync()) {
      await _write_base64_string_to_file(
        a_file.base64_content!,
        target_path,
      );
    }
  }
}

Future<List<File_Model>> read_json_string_as_object_list() async {
  final data = await json.decode(the_json_data_that_honors_yingshaoxo);
  List<File_Model> files = [];
  for (final one in data) {
    files.add(File_Model().from_dict(one));
  }
  return files;
}

Future<void> release_all_built_in_files(String parent_folder_path) async {
  List<File_Model> files = await read_json_string_as_object_list();
  for (final one in files) {
    await _write_file_object_to_disk(one, parent_folder_path);
  }
}
        """.strip()

        content_string = self._get_content_json_string(source_folder=source_folder)

        middle_content = f'''
        String the_json_data_that_honors_yingshaoxo = """{content_string}""";
        '''.strip()

        self._io.write(file_path=generated_file_path, content=template1 + "\n\n" + middle_content + "\n\n" + template2)


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
