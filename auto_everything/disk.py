from __future__ import annotations

from typing import Any, Iterable, List, Tuple

import os
import re
import json
import random
import string
import hashlib
import copy
import struct
import sys
import base64
import datetime
import shutil
from io import BytesIO

from dataclasses import dataclass
import pathlib
import tempfile
from pathlib import Path
import unicodedata
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


class Sha1():
    """A class that mimics that hashlib api and implements the SHA-1 algorithm."""

    def __init__(self):
        # Initial digest variables
        self._h = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

        # bytes object with 0 <= len < 64 used to store the end of the message
        # if the message length is not congruent to 64
        self._unprocessed = b''
        # Length in bytes of all data that has been processed so far
        self._message_byte_length = 0

    def _left_rotate(self, n, b):
        """Left rotate a 32-bit integer n by b bits."""
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    def _process_chunk(self, chunk, h0, h1, h2, h3, h4):
        """Process a chunk of data and return the new digest variables."""
        assert len(chunk) == 64

        w = [0] * 80

        # Break chunk into sixteen 4-byte big-endian words w[i]
        for i in range(16):
            w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]

        # Extend the sixteen 4-byte words into eighty 4-byte words
        for i in range(16, 80):
            w[i] = self._left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        # Initialize hash value for this chunk
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((self._left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                             a, self._left_rotate(b, 30), c, d)

        # Add this chunk's hash to result so far
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

        return h0, h1, h2, h3, h4

    def update(self, arg: bytes | bytearray):
        """Update the current digest.

        This may be called repeatedly, even after calling digest or hexdigest.

        Arguments:
            arg: bytes, bytearray, or BytesIO object to read from.
        """
        if isinstance(arg, (bytes, bytearray)):
            arg = BytesIO(arg)

        # Try to build a chunk out of the unprocessed data, if any
        chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))

        # Read the rest of the data, 64 bytes at a time
        while len(chunk) == 64:
            self._h = self._process_chunk(chunk, *self._h)
            self._message_byte_length += 64
            chunk = arg.read(64)

        self._unprocessed = chunk
        return self

    def digest(self):
        """Produce the final hash value (big-endian) as a bytes object"""
        return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

    def hexdigest(self):
        """Produce the final hash value (big-endian) as a hex string"""
        return '%08x%08x%08x%08x%08x' % self._produce_digest()

    def _produce_digest(self):
        """Return finalized digest variables for the data processed so far."""
        # Pre-processing:
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)

        # append the bit '1' to the message
        message += b'\x80'

        # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
        # is congruent to 56 (mod 64)
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)

        # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        # Process the final chunk
        # At this point, the length of the message is either 64 or 128 bytes.
        h = self._process_chunk(message[:64], *self._h)
        if len(message) == 64:
            return h
        return self._process_chunk(message[64:], *h)


class Sha256:
    # I recommend to use md5 or sha1, because this is slow for big file
    ks = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    hs = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    M32 = 0xFFFFFFFF

    def __init__(self, m = None):
        self.mlen = 0
        self.buf = b''
        self.k = self.ks[:]
        self.h = self.hs[:]
        self.fin = False
        if m is not None:
            self.update(m)

    @staticmethod
    def pad(mlen):
        mdi = mlen & 0x3F
        length = (mlen << 3).to_bytes(8, 'big')
        padlen = 55 - mdi if mdi < 56 else 119 - mdi
        return b'\x80' + b'\x00' * padlen + length

    @staticmethod
    def ror(x, y):
        return ((x >> y) | (x << (32 - y))) & Sha256.M32

    @staticmethod
    def maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def ch(x, y, z):
        return (x & y) ^ ((~x) & z)

    def compress(self, c):
        w = [0] * 64
        w[0 : 16] = [int.from_bytes(c[i : i + 4], 'big') for i in range(0, len(c), 4)]

        for i in range(16, 64):
            s0 = self.ror(w[i - 15],  7) ^ self.ror(w[i - 15], 18) ^ (w[i - 15] >>  3)
            s1 = self.ror(w[i -  2], 17) ^ self.ror(w[i -  2], 19) ^ (w[i -  2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & self.M32

        a, b, c, d, e, f, g, h = self.h

        for i in range(64):
            s0 = self.ror(a, 2) ^ self.ror(a, 13) ^ self.ror(a, 22)
            t2 = s0 + self.maj(a, b, c)
            s1 = self.ror(e, 6) ^ self.ror(e, 11) ^ self.ror(e, 25)
            t1 = h + s1 + self.ch(e, f, g) + self.k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & self.M32
            d = c
            c = b
            b = a
            a = (t1 + t2) & self.M32

        for i, (x, y) in enumerate(zip(self.h, [a, b, c, d, e, f, g, h])):
            self.h[i] = (x + y) & self.M32

    def update(self, m):
        if m is None or len(m) == 0:
            return

        assert not self.fin, 'Hash already finalized and can not be updated!'

        self.mlen += len(m)
        m = self.buf + m

        for i in range(0, len(m) // 64):
            self.compress(m[64 * i : 64 * (i + 1)])

        self.buf = m[len(m) - (len(m) % 64):]

    def digest(self):
        if not self.fin:
            self.update(self.pad(self.mlen))
            self.digest = b''.join(x.to_bytes(4, 'big') for x in self.h[:8])
            self.fin = True
        return self.digest

    def hexdigest(self):
        tab = '0123456789abcdef'
        return ''.join(tab[b >> 4] + tab[b & 0xF] for b in self.digest())


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
        return os.path.exists(path)
        #return Path(path).exists()
        #Path("").exists() will return True, which is not correct

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

        match = False
        for pattern in ignore_pattern_list:
            path_a = file_path.removeprefix(start_folder)
            patten_b = pattern.removeprefix("./")
            if fnmatch(path_a, patten_b):
                #print(path_a + " | " + patten_b)
                match = True
                break

        return match

    def get_gitignore_folders_and_files(self, folder: str, also_return_dot_git_folder: bool = False) -> list[str]:
        files = self.get_files(folder=folder)

        if "version" not in t.run_command("git --version").lower():
            print("error: git needs to get installed for using 'use_gitignore_file' paramater.")
            return files

        ignored_files = []
        git_folder_list = []
        for file in files:
            if "/.git/" in file:
                a_git_folder = file.split("/.git/")[0]
                if a_git_folder in git_folder_list:
                    continue
                else:
                    git_folder_list.append(a_git_folder)

                result = t.run_command(f"git ls-files --other --directory", cwd=a_git_folder).strip()
                if len(result) != 0:
                    if result.lower().startswith("fatal"):
                        continue
                    temp_files = result.split("\n")
                    temp_files = [self.join_paths(a_git_folder, one) for one in temp_files]
                    ignored_files += temp_files
        ignored_files = list(set(ignored_files))

        if also_return_dot_git_folder == True:
            dot_git_folder_files = []
            for file in files:
                if file not in ignored_files:
                    for git_folder in git_folder_list:
                        a_git_folder = git_folder + "/.git/"
                        if file.startswith(a_git_folder):
                            if a_git_folder not in dot_git_folder_files:
                                dot_git_folder_files.append(a_git_folder)
                                break
            ignored_files += dot_git_folder_files

        return ignored_files

    def get_gitignore_folders_and_files_by_using_yingshaoxo_method(self, folder: str, also_return_dot_git_folder: bool = False, include_docker_ignore_file: bool = False) -> list[str]:
        """
        Should not use it on top root folder, because it will use all gitignore for all sub_folders, which might have bugs.
        """
        final_path_list = []

        return_list_than_tree = False
        ignore_symbolic_link = True

        folder = self._expand_user(folder)

        root = _FileInfo(
            path=folder,
            is_folder=True,
            is_file=False,
            folder=self.get_directory_name(folder),
            name=self.get_file_name(folder),
            level=0,
            children=None
        )

        def dive(node, git_ignore_pattern_list = []):
            folder = node.path

            if not os.path.isdir(folder):
                return

            items = os.listdir(folder)
            if len(items) == 0:
                return

            ignore_pattern_list = git_ignore_pattern_list
            if ".gitignore" in items:
                temp_git_ignore_text = self.read_bytes_from_file(os.path.join(folder, ".gitignore")).decode("utf-8", errors="ignore")
                temp_git_ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=temp_git_ignore_text)
                ignore_pattern_list += temp_git_ignore_pattern_list
            if include_docker_ignore_file == True:
                if ".dockerignore" in items:
                    temp_git_ignore_text = self.read_bytes_from_file(os.path.join(folder, ".dockerignore")).decode("utf-8", errors="ignore")
                    temp_git_ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=temp_git_ignore_text)
                    ignore_pattern_list += temp_git_ignore_pattern_list
            ignore_pattern_list.append(".git")
            ignore_pattern_list = list(set(ignore_pattern_list))
            #print(ignore_pattern_list)

            files_and_folders: list[_FileInfo] = []
            for filename in items:
                file_path = os.path.join(folder, filename)

                if self._file_match_the_gitignore_rule_list(
                    start_folder=node.path,
                    file_path=file_path,
                    ignore_pattern_list=ignore_pattern_list,
                ):
                    final_path_list.append(file_path)
                    continue

                if ignore_symbolic_link == True:
                    if os.path.islink(file_path):
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
                dive(node=new_node, git_ignore_pattern_list=ignore_pattern_list)
                files_and_folders.append(
                    new_node
                )

            files_and_folders.sort(key=lambda node_: self._super_sort_key_function(node_.name))
            node.children = files_and_folders

        if also_return_dot_git_folder == True:
            dive(root, [".git"])
        else:
            dive(root, [])
        return final_path_list

    def get_files(
        self,
        folder: str,
        recursive: bool = True,
        type_limiter: List[str] | None = None,
        gitignore_text: str|None = None,
        use_gitignore_file: bool = False
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
        use_gitignore_file: bool
            if true, this function will not return any file/folder that matchs .gitignore file rules. And gitignore_text property will lose its effects.
        """
        folder = self._expand_user(folder)
        assert os.path.exists(folder), f"{folder} is not exist!"

        if use_gitignore_file == True:
            files = self.get_folder_and_files_with_gitignore(folder=folder, recursive=recursive, return_list_than_tree=True)
            new_files = []
            for file in files:
                ok = False
                if file.is_file == False:
                    continue
                if type_limiter == None:
                    ok = True
                else:
                    for type_limit in type_limiter:
                        if file.path.endswith(type_limit):
                            ok = True
                            break
                if ok == True:
                    new_files.append(file.path)
            return new_files

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
        gitignore_text: str|None = None,
        ignore_symbolic_link: bool = True
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

                if ignore_symbolic_link == True:
                    if os.path.islink(abs_folder_path):
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

                if ignore_symbolic_link == True:
                    if os.path.islink(abs_folder_path):
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
        ignore_symbolic_link: bool = True
    ) -> _FileInfo:
        """
        Get files and folders recursively under a folder.
        This function will return you a tree object as:
        ```
            @dataclass
            class _FileInfo:
                path: str
                is_folder: bool
                is_file: bool
                folder: str
                name: str
                level: int
                children: List[_FileInfo] | None = None
        ```

        Parameters
        ----------
        folder: string
        type_limiter: List[str]
            a list used to do a type filter, like [".mp3", ".epub"]
        gitignore_text: str
            similar to git's .gitignore file, if any file matchs any rule, it won't be inside of the 'return file list'
        """
        folder = self._expand_user(folder)

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

                    if ignore_symbolic_link == True:
                        if os.path.islink(file_path):
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

    def get_folder_and_files_with_gitignore(
        self,
        folder: str,
        recursive: bool = True,
        include_docker_ignore_file: bool = False,
        return_list_than_tree: bool = False,
        ignore_symbolic_link: bool = True
    ) -> _FileInfo | list[_FileInfo]:
        """
        Get files and folders recursively under a folder.
        This function will return you a tree object as:
        ```
            @dataclass
            class _FileInfo:
                path: str
                is_folder: bool
                is_file: bool
                folder: str
                name: str
                level: int
                children: List[_FileInfo] | None = None
        ```

        Parameters
        ----------
        folder: string
        recursive: bool = True,
        include_docker_ignore_file: bool = False,
        return_list_than_tree: bool = False,
        """
        folder = self._expand_user(folder)

        root = _FileInfo(
            path=folder,
            is_folder=True,
            is_file=False,
            folder=self.get_directory_name(folder),
            name=self.get_file_name(folder),
            level=0,
            children=None
        )

        def dive(node: _FileInfo, git_ignore_pattern_list: list[str] = []):
            folder = node.path

            if not os.path.isdir(folder):
                return

            items = os.listdir(folder)
            if len(items) == 0:
                return

            ignore_pattern_list = git_ignore_pattern_list
            if ".gitignore" in items:
                temp_git_ignore_text = self.read_bytes_from_file(os.path.join(folder, ".gitignore")).decode("utf-8", errors="ignore")
                temp_git_ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=temp_git_ignore_text)
                ignore_pattern_list += temp_git_ignore_pattern_list
            if include_docker_ignore_file == True:
                if ".dockerignore" in items:
                    temp_git_ignore_text = self.read_bytes_from_file(os.path.join(folder, ".dockerignore")).decode("utf-8", errors="ignore")
                    temp_git_ignore_pattern_list = self._parse_gitignore_text_to_list(gitignore_text=temp_git_ignore_text)
                    ignore_pattern_list += temp_git_ignore_pattern_list
            ignore_pattern_list.append(".git")
            ignore_pattern_list = list(set(ignore_pattern_list))
            #print(ignore_pattern_list)

            files_and_folders: list[_FileInfo] = []
            for filename in items:
                file_path = os.path.join(folder, filename)

                if self._file_match_the_gitignore_rule_list(
                    start_folder=node.path,
                    file_path=file_path,
                    ignore_pattern_list=ignore_pattern_list,
                ):
                    continue

                if ignore_symbolic_link == True:
                    if os.path.islink(file_path):
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
                if recursive == True:
                    dive(node=new_node, git_ignore_pattern_list=ignore_pattern_list)
                files_and_folders.append(
                    new_node
                )

            files_and_folders.sort(key=lambda node_: self._super_sort_key_function(node_.name))
            node.children = files_and_folders

        dive(root, [])

        if return_list_than_tree == False:
            return root
        else:
            result_list = []
            queue = [root]
            while len(queue) > 0:
                node = queue[0]
                queue = queue[1:]
                if node.children != None:
                    queue += node.children
                result_list.append(node)
            return result_list[1:]

    def sort_files_by_time(self, files: List[str], reverse: bool = False):
        files.sort(key=os.path.getmtime, reverse=reverse)
        return files

    def get_absolute_path(self, path: str) -> str:
        if path.startswith("~"):
            path = t.fix_path(path)

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

    def get_parent_directory_path(self, path: str):
        """
        /hi/you/abc.txt -> /hi/you
        /hi/you -> /hi
        """
        path = path.rstrip("/")
        path = self._expand_user(path)
        path = os.path.dirname(path)
        return path

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
        segment_size = 1024 * 1024 * 1
        path = self._expand_user(path)
        with open(path, "rb") as f:
            file_hash = hashlib.blake2s()
            while True:
                #data = f.read(8192)
                data = f.read(segment_size)
                if not data:
                    break
                file_hash.update(data)
        return file_hash.hexdigest()

    def get_hash_of_a_file_by_using_yingshaoxo_method(self, path: str, bytes_data: bytes | None = None, level: int = 1, length: int = 8, seperator: str = "_", with_size: bool = False) -> str:
        """
        get hash string based on the bytes of a file by using yingshaoxo method.
        this method works because a byte is a integer between (0, 255)

        Parameters
        ----------
        path: string
            the file path
        bytes_data: bytes
            the file bytes
        level: int
            how accurate it should be, only work for bytes_data. The higher the better.
        length: int
            default value is 8, but 1 would also be fine
        """
        """
        You could use it as "fuzz hash" by do the check for n parts of the file, then "".join() those result as a longer string
        For example:

        hash_code = disk.get_hash_of_a_file_by_using_yingshaoxo_method("", bytes_data=text.encode("utf-8"), level=128, length=10, seperator="")
        """
        dividor = (10 ** length) - 1
        seperator_length = len(seperator)

        if bytes_data != None:
            all_size = len(bytes_data)
            part_size = all_size // level
            if part_size == 0:
                raise Exception("The level is too high but the bytes_data is too small")
            if with_size == True:
                result_string = str(all_size) + seperator
            else:
                result_string = ""
            for level_i in range(level):
                start_index = level_i * part_size
                end_index = start_index + part_size
                file_hash = 0
                operator_flag = True
                for one_byte in bytes_data[start_index: end_index]:
                    if operator_flag == True:
                        file_hash += one_byte
                        operator_flag = False
                    else:
                        file_hash -= one_byte
                        operator_flag = True
                file_hash = file_hash % dividor
                file_hash = str(file_hash)
                file_hash = ('0' * (length - len(file_hash))) + file_hash
                result_string += file_hash + seperator
            if seperator_length == 0:
                return result_string
            else:
                return result_string[:-seperator_length]

        segment_size = 1024 * 1024 * 1
        path = self._expand_user(path)
        file_hash = 0
        all_size = 0
        with open(path, "rb") as f:
            operator_flag = True
            while True:
                #data = f.read(8192)
                data = f.read(segment_size)
                all_size += len(data)
                if not data:
                    break
                for one_byte in data:
                    if operator_flag == True:
                        file_hash += one_byte
                        operator_flag = False
                    else:
                        file_hash -= one_byte
                        operator_flag = True
        file_hash = file_hash % dividor
        file_hash = str(file_hash)
        file_hash = ('0' * (length - len(file_hash))) + file_hash
        if with_size == True:
            return str(all_size) + "_" + file_hash
        else:
            return file_hash

    def get_fuzz_hash_by_using_yingshaoxo_method(self, bytes_data: bytes, level: int = 256) -> str:
        hash_code = self.get_hash_of_a_file_by_using_yingshaoxo_method("", bytes_data=bytes_data, level=level, length=1, seperator="", with_size=True)
        return hash_code

    def get_simple_hash_of_a_file_by_using_yingshaoxo_method(self, path, bytes_data = None, level = 256, seperator = "_", with_size = False):
        """
        get simple hash string based on the bytes of a file by using yingshaoxo method.
        this method works because a byte is a integer between (0, 255)
        but you should not use it on integraty check, it is not a secure hash

        The core about this function is that it do a step check about a file, it collect a byte per 'all_length//level' bytes, all collected bytes togather becomes the hash code.

        Parameters
        ----------
        path: string
            the file path
        bytes_data: bytes
            the file bytes
        level: int
            how accurate it should be, only work for bytes_data. The higher the better.
        """
        real_level = level
        seperator_length = len(seperator)

        if bytes_data == None:
            file_ = open(path, "rb")
            bytes_data = file_.read()
            file_.close()

        all_size = len(bytes_data)
        if all_size == 0:
            return "_".join(['0' for one in list(range(real_level))])
        part_size = 0
        while part_size == 0:
            part_size = int(all_size / level)
            if part_size == 0:
                level = int(level / 2)

        result_list = []
        for level_i in range(level):
            the_index = level_i * part_size
            file_hash = str(int(bytes_data[the_index]))
            file_hash = ("0" * (3-len(file_hash))) + file_hash
            result_list.append(file_hash)

        result = seperator.join(result_list)
        if with_size == True:
            result = str(all_size) + seperator + result
        return result

    def get_hash_of_a_file_by_using_sha1(self, path: str) -> str:
        """
        get the sha1 hash string based on the bytes of a file.

        Parameters
        ----------
        path: string
            the file path
        """
        segment_size = 1024 * 1024 * 1
        path = self._expand_user(path)
        with open(path, "rb") as f:
            file_hash = hashlib.sha1()
            while True:
                #data = f.read(8192)
                data = f.read(segment_size)
                if not data:
                    break
                file_hash.update(data)
        return file_hash.hexdigest()

    def get_hash_of_a_folder(self, folder_path: str, print_log: bool = False) -> str:
        """
        get the sha1 hash string for a folder.

        Parameters
        ----------
        folder_path: string
            the folder path
        """
        folder_path = self._expand_user(folder_path)
        raw_files = self.get_files(folder_path)

        folder_list = []
        file_list = []
        for file in raw_files:
            if self.is_directory(file):
                folder_list.append(file)
            else:
                file_list.append(file)

        folder_list.sort()
        file_list.sort()

        general_hash = hashlib.sha1()

        for file in file_list:
            if print_log:
                print(file)
            general_hash.update(self.get_hash_of_a_file_by_using_sha1(file).encode("utf-8", errors="ignore"))
        for folder in folder_list:
            general_hash.update(folder.encode("utf-8", errors="ignore"))

        return general_hash.hexdigest()

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
        else:
            return bytes_size

    def get_folder_size(self, path: str, level: str = "B") -> int:
        """
        Get folder size in the unit of  B, KB, MB.
        Parameters
        ----------
        path: string
            the folder path
        level: string
            B, KB, or MB
        """
        folder_path = path
        total_size = 0

        for root, directories, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.stat(file_path).st_size
                total_size += file_size

            for directory in directories:
                directory_path = os.path.join(root, directory)
                directory_size = os.stat(directory_path).st_size
                total_size += directory_size

        if level == "B":
            return int("{:.0f}".format(total_size))
        elif level == "KB":
            return int("{:.0f}".format(total_size / float(1 << 10)))
        elif level == "MB":
            return int("{:.0f}".format(total_size / float(1 << 20)))
        else:
            return total_size

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

    def get_part_of_a_file_in_bytesio_format_from_a_file(self, file_path: str, file_segment_size_in_bytes: int, segment_number: int) -> BytesIO:
        if segment_number <= 0:
            raise Exception("segment_number should be > 0, for example, 1")
        with open(file_path, "rb") as fh:
            for _ in range(segment_number-1):
                fh.read(file_segment_size_in_bytes)
            buffer = BytesIO(fh.read(file_segment_size_in_bytes))
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
        if not self.exists(source_file_path):
            return
        if self.exists(target_file_path):
            os.remove(target_file_path)
        os.rename(source_file_path, target_file_path)

    def move_a_folder(self, source_folder_path: str, target_folder_path: str):
        source_folder_path = self._expand_user(source_folder_path)
        target_folder_path = self._expand_user(target_folder_path)
        if source_folder_path == target_folder_path:
            return
        if not self.exists(source_folder_path):
            return
        if self.exists(target_folder_path):
            self.delete_a_folder(target_folder_path)
        os.rename(source_folder_path, target_folder_path)

    def copy_a_file(self, source_file_path: str, target_file_path: str):
        source_file_path = self._expand_user(source_file_path)
        target_file_path = self._expand_user(target_file_path)
        if source_file_path == target_file_path:
            return
        self.create_a_folder(self.get_directory_path(target_file_path))
        shutil.copyfile(source_file_path, target_file_path)

    def convert_bytes_to_bytesio(self, bytes_data: bytes) -> BytesIO:
        bytes_io = BytesIO()
        bytes_io.write(bytes_data)
        bytes_io.seek(0)
        return bytes_io

    def create_a_folder(self, folder_path: str):
        folder_path = self._expand_user(folder_path)
        Path(folder_path).mkdir(parents=True, exist_ok=True)

    def copy_a_folder(self, source_folder_path: str, target_folder_path: str, use_gitignore_file: bool = False):
        source_folder_path = self._expand_user(source_folder_path)
        target_folder_path = self._expand_user(target_folder_path)

        source_folder_path = os.path.abspath(source_folder_path)
        target_folder_path = os.path.abspath(target_folder_path)

        if (not self.exists(target_folder_path)):
            self.create_a_folder(target_folder_path)
        else:
            if not self.is_directory(target_folder_path):
                self.delete_a_file(target_folder_path)

        if use_gitignore_file == True:
            source_files = self.get_folder_and_files_with_gitignore(folder=source_folder_path, recursive=True, return_list_than_tree=True)
            for source_file in source_files:
                sub_file_name = source_file.path[len(source_folder_path):]
                sub_file_name = sub_file_name.lstrip("/\\")
                target_file_path = self.join_paths(target_folder_path, sub_file_name)
                if source_file.is_folder:
                    self.create_a_folder(target_file_path)
                else:
                    #self.write_bytes_into_file(target_file_path, self.read_bytes_from_file(source_file.path))
                    self.copy_a_file(source_file.path, target_file_path)
            return

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

    def compress_bytes_by_using_yingshaoxo_method(self, bytes_data, window_length=1024) -> bytes:
        """
        A joke: A extreme compression method would be magnet torrent, a x GB file can be 'uncompressed' by a magnet hash link string.

        The real part is: if you use 'a' to represent 'ab', 'b' to represent 'ac', 'c' to represent 'ad', and so on, in the end, if you have a [ab,ac,ad] dict, you can always compress a file to its half size, but the price is you have to save that dict to everywhlere you want to uncompress a file.
        It is like, you can write light python code, but to execute it, the price is you have to spend big storage to save python interpreter, a binary file.

        Some compression software like rar, zip, 7z, they work in the same way, they rewrite the old file data, they make you can't get the original file unless you download their software.
        """
        text = self.bytes_to_base64(bytes_data)

        text_length = len(text)

        special_char_1 = chr(1)

        index = 0
        increasing_index = 0
        sub_string_hash_dict = {}
        data_list = []
        while True:
            sub_string = text[index: index+window_length]

            if sub_string in sub_string_hash_dict:
                data_list.append(sub_string_hash_dict[sub_string])
            else:
                sub_string_hash_dict[sub_string] = special_char_1 + str(increasing_index) + special_char_1
                increasing_index += 1
                data_list.append(sub_string)

            index += window_length
            if index >= text_length:
                break

        final_result = "".join(data_list)
        return final_result.encode("ascii")

    def uncompress_bytes_by_using_yingshaoxo_method(self, bytes_data, window_length=1024):
        data_list_string = bytes_data.decode("ascii")

        special_char_1 = chr(1)
        data_text_length = len(data_list_string)

        the_dict = {}
        the_list = []
        increasing_index = 0
        index = 0
        while True:
            if index >= data_text_length:
                break

            if data_list_string[index] == special_char_1:
                index_chars = ""
                temp_index = index + 1
                while True:
                    char = data_list_string[temp_index]
                    if char == special_char_1:
                        index = temp_index + 1
                        break
                    else:
                        index_chars += char
                    temp_index += 1
                the_list.append(int(index_chars))
                continue
            else:
                the_dict[increasing_index] = data_list_string[index: index+window_length]
                the_list.append(increasing_index)
                increasing_index += 1

            index += window_length
            if index >= data_text_length:
                break

        result_text = ""
        for one in the_list:
            result_text += the_dict[one]

        final_data = self.base64_to_bytes(result_text)
        return final_data



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
