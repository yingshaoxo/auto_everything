import string


class Password_Generator():
    """
    This is for hash password generation
    """

    def __init__(self, base_secret_string: str):
        """
        base_string: a base_string for PassWord generation
        """
        import hashlib
        self.hashlib = hashlib
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

        m = self.hashlib.sha512()
        m.update(self.__base_data)

        for data in data_list:
            m.update(data)

        result = m.hexdigest()
        result = result[:length - 1]
        # result = "A" + result
        return result


class EncryptionAndDecryption():
    def get_secret_alphabet_dict(self, a_secret_string: str) -> dict[str, str]:
        new_key = a_secret_string[::-1].replace(" ", "").lower()
        for char in new_key:
            if new_key.count(char) >= 2:
                new_key = new_key.replace(char, "", 1)
        a_secret_string = new_key[::-1]

        character_list = [char for char in a_secret_string if char.isalpha()]

        if len(character_list) >= 26:
            character_list = character_list[:26]
        else:
            characters_that_the_key_didnt_cover: list[str] = []
            for char in list(string.ascii_lowercase):
                if char not in character_list:
                    characters_that_the_key_didnt_cover.append(char)
            character_list = character_list + characters_that_the_key_didnt_cover

        final_dict: dict[str, str] = {}
        for index, char in enumerate(list(string.ascii_lowercase)):
            final_dict[char] = character_list[index]

        return final_dict

    def encode_message(self, a_secret_dict: dict[str, str], message: str) -> str:
        new_message: str = ""
        for char in message:
            if not char.isalpha():
                new_message += char
                continue
            new_char = a_secret_dict[char.lower()]
            if char.isupper():
                new_char = new_char.upper()
            new_message += new_char
        return new_message
    
    def decode_message(self, a_secret_dict: dict[str, str], message: str) -> str:
        new_secret_dict: dict[str, str] = {}
        for key, value in a_secret_dict.items():
            new_secret_dict[value] = key
        a_secret_dict = new_secret_dict

        new_message: str = ""
        for char in message:
            if not char.isalpha():
                new_message += char
                continue
            new_char = a_secret_dict[char.lower()]
            if char.isupper():
                new_char = new_char.upper()
            new_message += new_char
        return new_message


if __name__ == "__main__":
    pass