import json
import os


class IO():
    """
    This is for normal IO processing
    """

    def __init__(self):
        self.current_dir = os.getcwd()
        self.__log_path = os.path.join(self.current_dir, '.log')

    def make_sure_sudo_permission(self):
        """
        exit if you don't have sudo permission
        """
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()

    def read(self, file_path, auto_detect_encoding=False, encoding="utf-8"):
        """
        read text from txt file

        Parameters
        ----------
        file_path
            txt file path
        encoding
            utf-8 or ascii, ascii would be smaller for text storage
        """
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
            print("File '" + file_path + "' does not exists.")
            return ""

    def write(self, file_path, content, encoding="utf-8"):
        """
        write text into txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        encoding
            utf-8 or ascii, ascii would be smaller for text storage
        """
        with open(file_path, 'w', encoding=encoding, errors="ignore") as f:
            f.write(content)

    def append(self, file_path, content):
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

    def string_to_hex(self, utf_8_string):
        """
        Don't use hex, it adds complexity
        """
        return utf_8_string.encode("utf-8", errors="ignore").hex()

    def hex_to_string(self, hex_string):
        """
        Don't use hex, it adds complexity
        """
        return bytes.fromhex(hex_string).decode("utf-8", errors="ignore")

    def bytes_list_to_int_list(self, bytes_data):
        """
        a byte can be represented as a integer between 0 and 255.
        actually, if you loop python bytes object, you'll get a list of integer.
        > a number between 0 and 255 can be a chracter in ASCII table. I recommand use ASCII to save text data, because it is easy to read from bytes data from disk storage.
        """
        list_ = [None] * len(bytes_data)
        if type(bytes_data) == bytes or type(bytes_data) == bytearray:
            for index, int_byte in enumerate(bytes_data):
                list_[index] = int_byte
        else:
            for index, byte in enumerate(bytes_data):
                zero_and_one_string_for_one_byte = bin(byte)[2:]
                leading_zeros = ((8-len(zero_and_one_string_for_one_byte)) * '0')
                zero_and_one_string_for_one_byte = leading_zeros + zero_and_one_string_for_one_byte
                list_[index] = int(zero_and_one_string_for_one_byte, 2)
        return list_

    def int_list_to_bytes_list(self, int_list, big_or_little="little"):
        """
        a byte can be represented as a integer between 0 and 255
        to make it simple, you can think a byte as an integer in range of [0, 255]. actually, if you loop python bytes object, you'll get a list of integer.
        > a number between 0 and 255 can be a chracter in ASCII table

        The return bytearray object can get converted to bytes by using 'bytes(a_bytearray)'

        Why ask you to choose big or little?
        Let's assume you have a byte: 00000001, it is normal in your computer, it is 'little'
        But after you send it from right to left to another device, it becomes 10000000, it is 'big'. But if the other side do a reverse to let it become original data 00000001, they can still use 'little' to do the right parse.

        I think for those old generation of people, they are stupid. If they could use 'little' all the time by doing a list[::-1] at the other side in a communication, why they use 'big'?
        """
        use_little = True
        if big_or_little != "little":
            use_little = False

        a_bytearray = bytearray(range(len(int_list)))
        for index, int_between_0_and_255 in enumerate(int_list):
            if use_little:
                a_bytearray[index] = int_between_0_and_255
            else:
                a_bytearray[index] = int_between_0_and_255.to_bytes(2, big_or_little)[0]
        return a_bytearray

    def bytes_to_binary_zero_and_one(self, bytes_data):
        """
        Yes, a byte can be a integer in range of [0, 255], but if you want to send data over electrical line, you have to send 0 and 1 signal, which is 0v and 5v voltage.
        So you have to convert [0,255] number into a 8 length of string that only has 0 and 1.

        The return value is a list of zero and one string, similar to [00000001, 00000010, 00000011]

        Why for a byte, it has 8 number of zero or one? Because 2^8 == 256, you have to use 8 length of 0 and 1 to represent a number between 0 and 255 (a byte can represent a integer in range of [0,255])
        That's also why in C language, you use char or int to represent a byte. a byte is nothing but a integer between 0 and 255.

        > By the way, if you want to use 0 and 1 to represent a bigger number, for example 65536, you have to use 16 length of 0 and 1 number, because 2^16==65536.
        """
        list_ = [None] * len(bytes_data)
        for index, byte in enumerate(bytes_data):
            zero_and_one_string_for_one_byte = bin(byte)[2:]
            leading_zeros = ((8-len(zero_and_one_string_for_one_byte)) * '0')
            zero_and_one_string_for_one_byte = leading_zeros + zero_and_one_string_for_one_byte
            list_[index] = zero_and_one_string_for_one_byte
        return list_

    def binary_zero_and_one_to_bytes(self, zero_and_one_string_list):
        a_bytearray = bytearray(range(len(zero_and_one_string_list)))
        for index, binary_string in enumerate(zero_and_one_string_list):
            a_bytearray[index] = int(binary_string, 2)#.to_bytes(2, big_or_little)[0]
        return bytes(a_bytearray)

    def int_byte_to_binary_string(self, a_number):
        """
        For a byte or ascii number in range of [0,255], the binary_string should have 8 chracters, similar to 01100100
        """
        try:
            binary_string = format(a_number, "b")
            heading_zero = (8 - len(binary_string)) * '0'
            return heading_zero + binary_string
        except Exception as e:
            # yingshaoxo method of Hexadecimal conversion
            half_number_list = [[0,128], [0,64], [0,32], [0,16], [0,8], [0,4], [0,2], [0,1]]
            binary_string = ""
            for _, one in half_number_list:
                if a_number >= one:
                    binary_string += "1"
                    a_number -= one
                else:
                    binary_string += "0"
            return binary_string

    def string_binary_to_int_byte(self, binary_string):
        """
        For a byte or ascii number in range of [0,255], the binary_string should have 8 chracters, similar to 01100100
        Which means a byte has 8 characters. The binary_string length you gave to me should be 8.
        """
        try:
            return int(binary_string, 2)
        except Exception as e:
            half_number_list = [[0,128], [0,64], [0,32], [0,16], [0,8], [0,4], [0,2], [0,1]]
            the_number = 0
            index = 0
            for _, one in half_number_list:
                if binary_string[index] == "1":
                    the_number += one
                index += 1
            return the_number

    def __make_sure_txt_exist(self, path):
        if not os.path.exists(path):
            self.write(path, "")

    def read_settings(self, key, defult):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            data = json.loads(text)
            return data[key]
        except Exception as e:
            print(e)
            return defult

    def write_settings(self, key, value):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            try:
                data = json.loads(text)
            except Exception as e:
                print(e)
                data = dict()
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

    def log(self, text):
        import time
        text = str(text)
        now = time.asctime(time.localtime(time.time()))
        text = '\n' * 2 + text + '   ' + '({})'.format(now)
        self.append(self.__log_path, text)

    def get_logs(self):
        return self.read(self.__log_path)


class File_IO:
    def __init__(self, filename, mode=None):
        # 'wb' for write bytes but will clear the whole file first, 'w' for write string
        # 'rb+' for reading bytes and write bytes at any position
        # 'ab' for appending data at the end
        self.filename = filename

        if mode == None:
            if self.exists():
                mode = "rb+"
            else:
                mode = "wb+"
        self.mode = mode

        print(mode)
        self.file = open(filename, mode)

    def read(self, size=-1):
        return self.file.read(size)

    def write(self, data):
        if 'w' in self.mode or 'a' in self.mode or '+' in self.mode:
            self.file.write(data)

    def seek(self, offset, whence=None):
        # where to start: os.SEEK_END, start from end; os.SEEK_SET, start from beginning
        if whence == None:
            self.file.seek(offset)
        else:
            self.file.seek(offset, whence)

    def seek_from_end(self, negative_offset=0):
        # only support binary mode
        self.file.seek(negative_offset, os.SEEK_END)

    def tell(self):
        # get current file pointer that was set by seek
        return self.file.tell()

    def close(self):
        self.file.close()

    def get_size(self):
        try:
            return os.path.getsize(self.filename)
        except Exception as e:
            info = os.stat(self.filename)
            filesize = info[6]
            return filesize

    def exists(self):
        try:
            os.stat(self.filename)
            return True
        except Exception as e:
            return False

    def flush(self):
        self.file.flush()


class Yingshaoxo_List():
    def __init__(self):
        self.memory_slots_number = 16
        # create a list with 16 memory slots
        self.items = [None] * self.memory_slots_number
        self.length = 0

        self.iteration_not_done = False
        self._current_iterate_index = 0

    def _copy_old_items_to_new_items_based_on_memory_slots_number(self):
        new_items = [None] * self.memory_slots_number
        for i in range(self.length):
            new_items[i] = self.items[i]
        self.items = new_items

    def _double_the_memory_slots_number(self):
        self.memory_slots_number = self.memory_slots_number * 2
        self._copy_old_items_to_new_items_based_on_memory_slots_number()

    def _cut_half_the_memory_slots_number(self):
        new_slots_number = max(8, int(self.memory_slots_number / 2))
        if new_slots_number >= self.length:  # Ensure no data loss
            self.memory_slots_number = new_slots_number
            self._copy_old_items_to_new_items_based_on_memory_slots_number()

    def print(self):
        print("[", end="")
        for i in range(self.length):
            print(self.items[i], end="")
            if i != self.length - 1:
                print(", ", end="")
        print("]\n", end="")

    def append(self, an_element):
        if self.length >= self.memory_slots_number:
            # need to create a new list with self.memory_slots_number * 2 slots
            self._double_the_memory_slots_number()

        self.items[self.length] = an_element
        self.length += 1

    def index(self, an_element):
        for i in range(self.length):
            if self.items[i] == an_element:
                return i
        return None

    def delete(self, index):
        if index >= 0 and index < self.length:
            #del self.items[index]
            new_items = [None] * self.memory_slots_number
            new_index = 0
            for i in range(self.length):
                if i != index:
                    new_items[new_index] = self.items[i]
                    new_index += 1
            self.items = new_items
            self.length -= 1

        if self.length < int(self.memory_slots_number / 2):
            # need to create a new list with self.memory_slots_number / 2 slots
            self._cut_half_the_memory_slots_number()

    def set(self, index, an_element):
        if index < 0 or index >= self.length:
            return False
        else:
            self.items[index] = an_element
            return True

    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        return self.items[index]

    def insert(self, index, an_element):
        if index < 0 or index >= self.length:
            return

        if self.length >= self.memory_slots_number:
            # need to create a new list with self.memory_slots_number * 2 slots
            self._double_the_memory_slots_number()

        new_items = [None] * self.memory_slots_number
        new_index = 0
        for i in range(self.length):
            if i == index:
                new_items[new_index] = an_element
                new_index += 1
            new_items[new_index] = self.items[i]
            new_index += 1
        self.items = new_items
        self.length += 1

    def sublist(self, start_index, end_index):
        sub_list = Yingshaoxo_List()
        if start_index >= 0 and end_index <= self.length and start_index < end_index:
            for i in range(start_index, end_index):
                sub_list.append(self.items[i])
                # better do a copy for those values
        return sub_list

    def start_iteration(self):
        # most of the time, it is True
        self.iteration_not_done = self.length > 0
        self._current_iterate_index = 0

    def get_next_one(self):
        if not self.iteration_not_done or self._current_iterate_index >= self.length:
            self.iteration_not_done = False
            return None

        an_element = self.items[self._current_iterate_index]
        self._current_iterate_index += 1

        if self._current_iterate_index >= self.length:
            self.iteration_not_done = False

        return an_element


class Yingshaoxo_Dict():
    """
    This dict is based on yingshaoxo hash table algorithm.
    """
    def __init__(self, second_level=False):
        self.key_and_value_distribution_list = [None] * 255
        self.second_level = second_level
        if second_level == True:
            for i in range(255):
                # for each branch, it has [key_list, value_list]
                self.key_and_value_distribution_list[i] = [
                    [], []
                ]
        else:
            for i in range(255):
                self.key_and_value_distribution_list[i] = Yingshaoxo_Dict(second_level=True)

    def _get_yingshaoxo_hash_id_of_a_string_for_the_first_level(self, key):
        """
        It returns a index between [0, 254]
        """
        key = str(key)
        return (ord(key[0]) + ord(key[-1])) % 255

    def _get_yingshaoxo_hash_id_of_a_string(self, key):
        """
        It returns a index between [0, 254]
        """
        key = str(key)
        #return ord(key[int(len(key)/2)]) % 255
        hash_id = 0
        sign = True
        for byte in key[::3].encode("utf-8"):
            if sign == True:
                hash_id += byte
            else:
                hash_id -= byte
            sign = not sign
        hash_id = hash_id % 255
        return hash_id

    def set(self, key, value):
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            # python pass list as pointer, so we will change original list
            keys, values = self.key_and_value_distribution_list[hash_id]
            for index, old_key in enumerate(keys):
                if old_key == key:
                    values[index] = value
                    return
            keys.append(key)
            values.append(value)
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            a_dict.set(key, value)

    def get(self, key):
        """
        If not exists, we return None
        """
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            keys, values = self.key_and_value_distribution_list[hash_id]
            for index, old_key in enumerate(keys):
                if old_key == key:
                    return values[index]
            return None
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            return a_dict.get(key)

    def delete(self, key):
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            keys, values = self.key_and_value_distribution_list[hash_id]
            target_index = None
            for index, old_key in enumerate(keys):
                if old_key == key:
                    target_index = index
                    break
            if target_index != None:
                del keys[target_index]
                del values[target_index]
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            a_dict.delete(key)

    def has_key(self, key):
        if self.second_level == True:
            if self.get(key) == None:
                return False
            else:
                return True
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            return a_dict.has_key(key)


class Yingshaoxo_Pure_String_Dict():
    def __init__(self):
        self.raw_string = ""
        self._init_splitor()

    def _init_splitor(self, splitor1=".#line#.", splitor2="|#colon#|"):
        self.splitor1 = splitor1
        self.splitor2 = splitor2

    def set_value_by_key(self, key, value):
        if self.has_key(key):
            # modifying
            search_string = self.splitor1 + key + self.splitor2
            index1 = self.raw_string.find(search_string)
            if index1 == -1:
                return
            self.raw_string = self.raw_string[:index1] + value + self.raw_string[index1+len(value):]
        else:
            # add new
            self.raw_string += self.splitor1 + key + self.splitor2 + value

    def has_key(self, key):
        if (self.splitor1 + key + self.splitor2) in self.raw_string:
            return True
        else:
            return False

    def get_value_by_key(self, key):
        search_string = self.splitor1 + key + self.splitor2
        index1 = self.raw_string.find(search_string)
        if index1 == -1:
            return None
        rest_string = self.raw_string[index1 + len(search_string):]
        index2 = rest_string.find(self.splitor1)
        if index2 == -1:
            return rest_string
        else:
            return rest_string[:index2]

    def delete_a_key(self, key):
        search_string = self.splitor1 + key + self.splitor2
        index1 = self.raw_string.find(search_string)
        if index1 == -1:
            return

        rest_string = self.raw_string[index1 + len(search_string):]
        index2 = rest_string.find(self.splitor1)
        if index2 == -1:
            self.raw_string = self.raw_string[:index1]
        else:
            self.raw_string = self.raw_string[:index1] + rest_string[index2:]

    def get_keys(self):
        lines = self.raw_string.split(self.splitor1)
        elements = []
        for line in lines[1:]:
            a_key = line.split(self.splitor2)[0]
            elements.append(a_key)
        return elements

    def get_keys_and_values(self):
        lines = self.raw_string.split(self.splitor1)
        elements = []
        for line in lines[1:]:
            elements.append(line.split(self.splitor2))
        return elements

    def dumps(self):
        return self.raw_string

    def loads(self, a_string):
        self.raw_string = a_string


class Redis_Style_Disk_String_Dict():
    """
    # author: baidu deepseek v3

    # needs: yingshaoxo

        Is there a disk_dict in python that can the place of dict, allow using dict on the hard drive to reduce memory usage?

        I looked at some packages, but they all have dependencies, which is unreliable. I need a single-file, no-dependency python file. I don't need type annotations; Can this thing take up almost 0 memory? My data keys are also super large, so nothing can be in memory; everything must rely on the disk.

        Can you let the following code support "a b c d e f g ..." sub_folder split? So the search speed of key will increase, and will bypass the max_files number a folder can save problem.

        Can you create your own hash method than using hashlib or zlib? the python hashlib is not stable according to my experience.

        Can you make the whole class not rely on pickle? Can you just save and read pure string? We also do not need json. You can assume all stuff we save is str type, you can also use str() to force do a conversion if you like.

        We actually need a disk dict that supports putting another dict in dict. It is like the value can be a value or key_list.
    """
    __slots__ = ('_path', '_depth')

    def __init__(self, path, depth=2):
        self._path = path
        self._depth = depth
        os.makedirs(self._path, exist_ok=True)

    def _custom_hash(self, data):
        """FNV-1a hash implementation using format()"""
        if not isinstance(data, str):
            data = str(data)
        data = data.encode('utf-8')

        fnv_prime = 0x01000193
        hash_val = 0x811c9dc5

        for byte in data:
            hash_val ^= byte
            hash_val = (hash_val * fnv_prime) & 0xffffffff

        return '{0:08x}'.format(hash_val)

    def _get_subfolder_path(self, key_hash):
        """Build nested folder structure"""
        path = self._path
        for i in range(self._depth):
            path = os.path.join(path, key_hash[i*2:(i+1)*2])
        return path

    def _key_path(self, key):
        """Generate complete filesystem path"""
        key_hash = self._custom_hash(key)
        base_path = self._get_subfolder_path(key_hash)
        os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, key_hash)

    def __setitem__(self, key, value):
        """Store key-value pair"""
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(value, str):
            value = str(value)

        base_path = self._key_path(key)
        temp_path = '{0}.tmp'.format(base_path)
        final_key_path = '{0}.key'.format(base_path)
        final_val_path = '{0}.val'.format(base_path)

        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(key)
            os.replace(temp_path, final_key_path)

            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(value)
            os.replace(temp_path, final_val_path)
        except Exception:
            try: os.remove(temp_path)
            except: pass
            raise

    def get(self, key):
        try:
            return self.__getitem__(key)
        except Exception as e:
            return None

    def __getitem__(self, key):
        """Retrieve value by key"""
        if not isinstance(key, str):
            key = str(key)

        base_path = self._key_path(key)
        try:
            with open('{0}.key'.format(base_path), 'r', encoding='utf-8') as f:
                disk_key = f.read()
            if disk_key != key:
                raise KeyError(key)

            with open('{0}.val'.format(base_path), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise KeyError(key)

    def __delitem__(self, key):
        """Delete key-value pair"""
        if not isinstance(key, str):
            key = str(key)

        base_path = self._key_path(key)
        try:
            os.remove('{0}.key'.format(base_path))
            os.remove('{0}.val'.format(base_path))
        except FileNotFoundError:
            raise KeyError(key)

    def __contains__(self, key):
        """Check if key exists"""
        try:
            self[key]
            return True
        except KeyError:
            return False

    def clear(self):
        """Remove all stored items"""
        for root, _, files in os.walk(self._path):
            for fname in files:
                if fname.endswith(('.key', '.val')):
                    os.remove(os.path.join(root, fname))

    def __iter__(self):
        """Iterate through all keys"""
        for root, _, files in os.walk(self._path):
            for fname in files:
                if fname.endswith('.key'):
                    try:
                        with open(os.path.join(root, fname), 'r', encoding='utf-8') as f:
                            yield f.read()
                    except UnicodeDecodeError:
                        continue


class Disk_Dict():
    # author: yingshaoxo
    def __init__(self, folder_path, id_="0", depth=1):
        self.folder_path = folder_path
        self.dict_register_folder = os.path.join(folder_path, "dict_register_folder")
        self.dict_data_folder = os.path.join(folder_path, "dict_data_folder")
        self.id_ = id_

        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(self.dict_register_folder, exist_ok=True)
        os.makedirs(self.dict_data_folder, exist_ok=True)

        if depth > 4:
            depth = 4
        self.register_dict = Redis_Style_Disk_String_Dict(self.dict_register_folder, depth)
        self.data_dict = Redis_Style_Disk_String_Dict(self.dict_data_folder, depth)

        register_increasing_id = self.register_dict.get("register_increasing_id")
        if register_increasing_id == None:
            self.register_dict["register_increasing_id"] = id_

        if self.id_ not in self.register_dict:
            self.register_dict[self.id_] = ""

    def _safe_string(self, input_text):
        # the space may also be a dangerous one, because it can get removed by strip()
        return input_text.replace(",", "/comma")

    def _unsafe_string(self, input_text):
        return input_text.replace("/comma", ",")

    def clear_all_data_for_all_dict_including_parent_dict(self):
        import shutil
        shutil.rmtree(self.folder_path)
        self.__init__(self.folder_path, id_="0")

    def create_a_new_dict(self):
        register_increasing_id = self.register_dict.get("register_increasing_id")
        new_id_string = str(int(register_increasing_id) + 1)
        self.register_dict["register_increasing_id"] = new_id_string
        new_dict = Disk_Dict(self.folder_path, new_id_string)
        return new_dict

    def __setitem__(self, key, value):
        key = self._safe_string(key)
        value_copy = value
        if type(value) == str:
            # v: is a value
            value = "v:" + value
        elif type(value) == Disk_Dict:
            # a: is a reference for another dict
            value = "a:" + value.id_
        elif type(value) == dict:
            a_dict = self.create_a_new_dict()
            value = "a:" + a_dict.id_
            # a: is a reference for another dict
            for key_, value_ in value_copy.items():
                a_dict[key_] = value_

        new_key = self.id_ + ":" + key
        self.data_dict[new_key] = value

        # the following may slow down the setting speed when the key is a lot in a dict
        new_key_list_string = ""
        if self.id_ in self.register_dict:
            new_key_list_string = self.register_dict[self.id_]

        if ","+new_key in new_key_list_string:
            # it already in there
            return None

        new_key_list_string += "," + new_key
        if new_key_list_string.startswith(",,"):
            new_key_list_string = new_key_list_string[1:]
        self.register_dict[self.id_] = new_key_list_string

    def __getitem__(self, key):
        key = self._safe_string(key)
        new_key = self.id_ + ":" + key
        value = self.data_dict.get(new_key)
        if value == None:
            return None

        if value.startswith("v:"):
            # v: is a value
            return value[2:]
        elif value.startswith("a:"):
            # a: is a reference for another dict
            id_ = value[2:]
            return Disk_Dict(self.folder_path, id_=id_)

    def get(self, key):
        key = self._safe_string(key)
        try:
            return self.__getitem__(key)
        except Exception as e:
            return None

    def __delitem__(self, key):
        key = self._safe_string(key)
        try:
            # clear child dict first if that item is a dict
            the_value_that_should_be_deleted = self.__getitem__(key)
            if type(the_value_that_should_be_deleted) == Disk_Dict:
                the_value_that_should_be_deleted.clear()

            new_key = self.id_ + ":" + key
            self.data_dict.__delitem__(new_key)

            new_key_list_string = self.register_dict[self.id_]
            self.register_dict[self.id_] = new_key_list_string.replace(","+new_key, "")
        except Exception as e:
            pass

    def __contains__(self, key):
        key = self._safe_string(key)
        new_key = self.id_ + ":" + key
        return self.data_dict.__contains__(new_key)

    def __iter__(self):
        # not work
        new_key_list_string = self.register_dict[self.id_]
        new_key_list_string = new_key_list_string.strip(",")
        real_new_key_list = [one for one in new_key_list_string.split(",") if one != ""]
        pre_length = len(self.id_+":")
        for new_key in real_new_key_list[1:]:
            yield new_key[pre_length:]

    def keys(self):
        new_key_list_string = self.register_dict[self.id_]
        new_key_list_string = new_key_list_string.strip(",")
        real_new_key_list = new_key_list_string.split(",")
        pre_length = len(self.id_+":")
        return [self._unsafe_string(one[pre_length:]) for one in real_new_key_list]

    def clear(self):
        a_key_list = self.keys()
        for key in a_key_list:
            self.__delitem__(key)


"""
class Disk_Saver_Dict():
    # This class will 100% have bugs, will not working right.
    # Currently, the method for doing the same thing is: 1.split word and put it into word_dict first in another file, 2.save id number directly in Disk_Dict() class.

    # Our disk dict is different than others, we can save space by reuse dict_data_folder's data
    # If you use this class to save tree data, it will reuse node value, so in the end, the whole tree will be reuse all node value as address reference. That is why it saves disk sapce.
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.register_increasing_id_dict_folder = os.path.join(folder_path, "register_increasing_id_dict_folder")
        self.base_element_to_id_dict_folder = os.path.join(folder_path, "base_element_to_id_dict_folder")
        self.id_to_base_element_dict_folder = os.path.join(folder_path, "id_to_base_element_dict_folder")
        self.tree_dict_folder = os.path.join(folder_path, "tree_dict_folder")

        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(self.register_increasing_id_dict_folder, exist_ok=True)
        os.makedirs(self.base_element_to_id_dict_folder, exist_ok=True)
        os.makedirs(self.id_to_base_element_dict_folder, exist_ok=True)
        os.makedirs(self.tree_dict_folder, exist_ok=True)

        self.register_increasing_id_dict = Redis_Style_Disk_String_Dict(self.register_increasing_id_dict_folder, 1)
        self.base_element_to_id_dict = Redis_Style_Disk_String_Dict(self.base_element_to_id_dict_folder, 3)
        self.id_to_base_element_dict = Redis_Style_Disk_String_Dict(self.id_to_base_element_dict_folder, 3)
        self.tree_dict = Disk_Dict(self.tree_dict_folder)

        if "id" not in self.register_increasing_id_dict["id"]:
            self.register_increasing_id_dict["id"] = "0"

    def _set_base_element(self, key_or_value):
        # return element_id_string
        id_string = self.base_element_to_id_dict.get(key_or_value)
        if id_string == None:
            # need to add a new id
            new_id = str(int(self.register_increasing_id_dict["id"]) + 1)
            self.id_to_base_element_dict[new_id] = key_or_value
            self.base_element_to_id_dict[key_or_value] = new_id
            self.register_increasing_id_dict["id"] = new_id
        else:
            return id_string

    def _get_base_element(self, element_id_string):
        # could be None, return raw_string
        raw_string = self.id_to_base_element_dict.get(element_id_string)
        if raw_string == None:
            return ""
        else:
            return raw_string

    def clear_all_data_for_all_dict_including_parent_dict(self):
        self.tree_dict.clear_all_data_for_all_dict_including_parent_dict()
        self.register_increasing_id_dict_folder.clear()
        self.base_element_to_id_dict.clear()
        self.id_to_base_element_dict.clear()

    def __setitem__(self, key, value):
        key_id = self._set_base_element(key)
        value_id = self._set_base_element(value)
        self.tree_dict.__setitem__(key_id, value_id)

    def __getitem__(self, key):
        key_id = self._set_base_element(key)
        result = self.tree_dict.__getitem__(key_id)
        if result == None:
            return result
        else:
            result = self._get_base_element(result)
            return result

    def get(self, key):
        return self.__getitem__(key)

    def __delitem__(self, key):
        key_id = self._set_base_element(key)
        return self.tree_dict.__delitem__(key_id)

    def __contains__(self, key):
        key_id = self._set_base_element(key)
        return self.tree_dict.__contains__(key_id)

    def keys(self):
        the_keys = self.tree_dict.keys()
        return [self._get_base_element(one) for one in the_keys]
"""


class MyIO():
    def __init__(self):
        import io
        import hashlib
        import base64
        self.io = io
        self.hashlib = hashlib
        self.base64 = base64

    def string_to_md5(self, text):
        result = self.hashlib.md5(text.encode())
        return result.hexdigest()

    def base64_to_bytesio(self, base64_string):
        img_data = self.base64.b64decode(base64_string)
        return self.io.BytesIO(img_data)

    def bytesio_to_base64(self, bytes_io):
        """
        bytes_io: io.BytesIO()
        """
        bytes_io.seek(0)
        return self.base64.b64encode(bytes_io.getvalue()).decode()

    def hex_to_bytes(self, hex_string):
        return bytes.fromhex(hex_string)

    def bytes_to_hex(self, bytes_data):
        """
        bytes_data: bytes()
        """
        return bytes_data.hex()


if __name__ == "__main__":
    pass
    """
    io = IO()
    zero_and_one_list = io.bytes_to_binary_zero_and_one(b"123")
    print(zero_and_one_list)
    bytes_list = io.binary_zero_and_one_to_bytes(zero_and_one_list)
    print(bytes_list)
    int_list = io.bytes_list_to_int_list(bytes_list)
    print(int_list)
    new_bytes_list = io.int_list_to_bytes_list(int_list)
    int_list = io.bytes_list_to_int_list(new_bytes_list)
    print(int_list)
    """
    """
    a_dict = Yingshaoxo_Dict()
    print(a_dict.get("hi"))
    a_dict.set("hi", "yingshaoxo")
    print(a_dict.get("hi"))
    a_dict.set("hi", "everyone")
    print(a_dict.get("hi"))
    a_dict.delete("hi")
    print(a_dict.get("hi"))
    """
    """
    a_list = Yingshaoxo_List()
    a_list.print()
    a_list.append(1)
    a_list.append(2)
    a_list.append(3)
    a_list.print()
    print(a_list.index(3))
    a_list.set(2,'hi')
    a_list.print()
    a_list.delete(0)
    a_list.print()
    a_list.insert(0, 0)
    a_list.print()
    print(a_list.get(3))
    a_list.append(4)
    a_list.print()
    a_list.sublist(0,4).print()

    a_list.start_iteration()
    while (a_list.iteration_not_done):
        an_element = a_list.get_next_one()
        print(an_element)
    """
