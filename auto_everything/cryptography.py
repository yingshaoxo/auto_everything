from typing import Any

import random
import string
import hashlib
import base64
import json


class JWT_Tool():
    def my_jwt_encode(self, data: dict[str, Any], a_secret_string_for_integrity_verifying: str, use_md5: bool = True) -> str:
        """
        return the jwt string. it should only be used as a temporary password, you should not contain any sensitive information in it.

        Parameters
        ----------
        data: 
            a_dict, which contains the real information

        a_secret_string_for_integrity_verifying: string
            a secret string
        """
        header = {
            "alg": "SHA256",
            "typ": "JWT"
        }
        if (use_md5):
            header["alg"] = "MD5"
        header_base64_string = base64.b64encode(json.dumps(header).encode(encoding="utf-8")).decode("ascii")

        payload = data
        payload_base64_string = base64.b64encode(json.dumps(payload).encode(encoding="utf-8")).decode("ascii")

        if (use_md5):
            m = hashlib.md5()
        else:
            m = hashlib.sha256()

        m.update((header_base64_string + "." + payload_base64_string + "." + a_secret_string_for_integrity_verifying).encode(encoding="utf-8"))
        signature_ = m.hexdigest()

        return header_base64_string + "." + payload_base64_string + "." + signature_

    def my_jwt_decode(self, jwt_string: str, a_secret_string_for_integrity_verifying: str) -> dict[str, Any] | None:
        """
        return `None` if verifying didn't pass

        Parameters
        ----------
        jwt_string: 
            any string

        a_secret_string_for_integrity_verifying: string
            a secret string
        """
        try:
            splits = jwt_string.split(".")
            if len(splits) != 3:
                return None
            
            header = json.loads(base64.b64decode(splits[0]).decode(encoding="utf-8")) 
            header_base64_string = base64.b64encode(json.dumps(header).encode(encoding="utf-8")).decode("ascii")

            payload = json.loads(base64.b64decode(splits[1]).decode(encoding="utf-8"))
            payload_base64_string = base64.b64encode(json.dumps(payload).encode(encoding="utf-8")).decode("ascii")

            if (header['alg'] == "MD5"):
                m = hashlib.md5()
            else:
                m = hashlib.sha256()

            m.update((header_base64_string + "." + payload_base64_string + "." + a_secret_string_for_integrity_verifying).encode(encoding="utf-8"))
            signature_ = m.hexdigest()

            if signature_ == splits[2]:
                return payload
            else:
                return None
        except Exception as e:
            print(f"error: {e}")
            return None


class Password_Generator():
    """
    This is for hash password generation
    """

    def __init__(self, base_secret_string: str):
        """
        base_string: a base_string for PassWord generation
        """
        self.__base_data = base_secret_string.encode("utf-8")

    def get_password(self, secret_string_list: list[str], length: int = 12):
        """
        return a hashed string based on the text you were given
        you can use the returned string as your password

        Parameters
        ----------
        secret_string_list: 
            any string

        length: int
            password length
        """
        if (len(secret_string_list) == 0):
            raise Exception("You should give me at least one secret string in secret_string_list")

        data_list = [string.encode("utf-8") for string in secret_string_list]

        m = hashlib.sha512()
        m.update(self.__base_data)

        for data in data_list:
            m.update(data)

        result = m.hexdigest()
        result = result[:length - 1]
        # result = "A" + result
        return result

    def get_random_password(self, 
                            use_numbers: bool = True, 
                            use_ascii_lowercase_characters: bool = True, 
                            use_ascii_uppercase_characters: bool = True, 
                            use_punctuation: bool = False, 
                            additional_string_at_head: str = "",
                            length: int = 12):
        """
        return a random string, you can use the returned string as your password

        Parameters
        ----------
        additional_string_at_head: str
            You can put some string like '@yingshaoxo_' in this argument, so for each password you get, it will start with '@yingshaoxo_'

        length: int
            password length
        """
        characters_list: list[str] = []
        if (use_numbers == True):
            characters_list += list(string.digits)
        if (use_ascii_lowercase_characters == True):
            characters_list += list(string.ascii_lowercase)
        if (use_ascii_uppercase_characters == True):
            characters_list += list(string.ascii_uppercase)
        if (use_punctuation == True):
            characters_list += list(string.punctuation)
        result = ''.join(random.choices(characters_list, k=length))
        return additional_string_at_head + result


class EncryptionAndDecryption():
    def get_secret_alphabet_dict(self, a_secret_string: str) -> dict[str, str]:
        a_secret_string = a_secret_string.replace(" ", "").lower()
        character_list: list[str] = []
        for char in a_secret_string:
            if char.isalpha():
                if char not in character_list:
                    character_list.append(char)

        if len(character_list) >= 26:
            character_list = character_list[:26]
        else:
            characters_that_the_key_didnt_cover: list[str] = []
            for char in list(string.ascii_lowercase):
                if char not in character_list:
                    characters_that_the_key_didnt_cover.append(char)
            character_list = character_list + characters_that_the_key_didnt_cover

        final_dict: dict[str, str] = {}

        # for alphabet
        for index, char in enumerate(list(string.ascii_lowercase)):
            final_dict[char] = character_list[index]
        
        # for numbers
        original_numbers_in_alphabet_format = list(string.ascii_lowercase)[:10] #0-9 representations in alphabet format
        secret_numbers_in_alphabet_format = list(final_dict.values())[:10]
        final_number_list: list[str] = []
        for index in range(0, 10):
            secret_char = secret_numbers_in_alphabet_format[index]
            if secret_char in original_numbers_in_alphabet_format:
                final_number_list.append(str(original_numbers_in_alphabet_format.index(secret_char)))
        if len(final_number_list) >= 10:
            final_number_list = final_number_list[:10]
        else:
            numbers_that_didnt_get_cover: list[str] = []
            for char in range(0, 10):
                char = str(char)
                if char not in final_number_list:
                    numbers_that_didnt_get_cover.append(char)
            final_number_list = final_number_list + numbers_that_didnt_get_cover
        for index, char in enumerate(final_number_list):
            final_dict[str(index)] = char
        
        return final_dict

    def encode_message(self, a_secret_dict: dict[str, str], message: str) -> str:
        new_message: str = ""
        for char in message:
            if (not char.isalpha()) and (not char.isnumeric()):
                new_message += char
                continue
            if char in a_secret_dict.keys():
                new_char = a_secret_dict[char.lower()]
                if char.isupper():
                    new_char = new_char.upper()
            else:
                new_char = char
            new_message += new_char
        return new_message
    
    def decode_message(self, a_secret_dict: dict[str, str], message: str) -> str:
        new_secret_dict: dict[str, str] = {}
        for key, value in a_secret_dict.items():
            new_secret_dict[value] = key
        a_secret_dict = new_secret_dict

        new_message: str = ""
        for char in message:
            if (not char.isalpha()) and (not char.isnumeric()):
                new_message += char
                continue
            if char in a_secret_dict.keys():
                new_char = a_secret_dict[char.lower()]
                if char.isupper():
                    new_char = new_char.upper()
            else:
                new_char = char
            new_message += new_char
        return new_message


if __name__ == "__main__":
    # encryption_and_decryption = EncryptionAndDecryption()

    # a_dict = encryption_and_decryption.get_secret_alphabet_dict("hello, world")

    # a_sentence = "I'm yingshaoxo. Here is the test number: 9111108848."

    # encrypted_sentence = encryption_and_decryption.encode_message(a_secret_dict=a_dict, message=a_sentence)
    # print()
    # print(encrypted_sentence)

    # decrypted_sentence = encryption_and_decryption.decode_message(a_secret_dict=a_dict, message=encrypted_sentence)
    # print(decrypted_sentence)


    # password_generator = Password_Generator("yingshaoxo")
    # print(password_generator.get_random_password(use_punctuation=False, additional_string_at_head="@yingshaoxo_"))


    jwt_tool  = JWT_Tool()

    secret = "secret is a secret"

    a_jwt_string = jwt_tool.my_jwt_encode(data={"name": "yingshaoxo"}, a_secret_string_for_integrity_verifying=secret, use_md5=True)
    print(a_jwt_string)

    original_dict = jwt_tool.my_jwt_decode(jwt_string=a_jwt_string, a_secret_string_for_integrity_verifying=secret)
    print(original_dict)

    fake_jwt_string = "eyJhbGciOiAiU0hBMjU2IiwgInR5cCI6ICJKV1QifQ==.eyJuYW1lIjogInlpbmdzaGFveG8ifQ==.53c4df02e99e2ce3d3f8d230c799e9f0cbe9963e484b45efe171f38ebe58d690"
    original_dict = jwt_tool.my_jwt_decode(jwt_string=fake_jwt_string, a_secret_string_for_integrity_verifying=secret)
    print(original_dict)