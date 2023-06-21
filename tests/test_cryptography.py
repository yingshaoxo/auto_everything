from auto_everything.cryptography import Encryption_And_Decryption, Password_Generator, JWT_Tool


def test_password():
    password_generator = Password_Generator(base_secret_string="yingshaoxo")
    password = password_generator.get_password(secret_string_list=["hi"])
    print(password)


def test_strong_password():
    password_generator = Password_Generator("yingshaoxo")
    print(password_generator.get_random_password(use_punctuation=False, additional_string_at_head="@yingshaoxo_"))
    

def test_cryptography():
    encryption_and_decryption = Encryption_And_Decryption()

    a_dict = encryption_and_decryption.get_secret_alphabet_dict("yingshaoxo is the best")
    print(a_dict)

    a_sentence = "Hello, world, I'm yingshaoxo. Here is the test number: 9111108848."

    encrypted_sentence = encryption_and_decryption.encode_message(a_secret_dict=a_dict, message=a_sentence)
    print()
    print(encrypted_sentence)

    decrypted_sentence = encryption_and_decryption.decode_message(a_secret_dict=a_dict, message=encrypted_sentence)
    print(decrypted_sentence)


def test_encryption():
    encryption_and_decryption = Encryption_And_Decryption()

    a_dict = encryption_and_decryption.get_secret_alphabet_dict("Asking is not a bad thing if the person you ask are comfortable with it.")
    print(a_dict)

    a_sentence = "yingshaoxo@gmail.com"

    encrypted_sentence = encryption_and_decryption.encode_message(a_secret_dict=a_dict, message=a_sentence)
    print()
    print(encrypted_sentence)

    decrypted_sentence = encryption_and_decryption.decode_message(a_secret_dict=a_dict, message=encrypted_sentence)
    print(decrypted_sentence)


def test_jwt():
    jwt_tool  = JWT_Tool()

    secret = "secret is a secret"

    a_jwt_string = jwt_tool.my_jwt_encode(data={"name": "yingshaoxo"}, a_secret_string_for_integrity_verifying=secret, use_md5=True)
    print(a_jwt_string)

    original_dict = jwt_tool.my_jwt_decode(jwt_string=a_jwt_string, a_secret_string_for_integrity_verifying=secret)
    print(original_dict)

    fake_jwt_string = "eyJhbGciOiAiU0hBMjU2IiwgInR5cCI6ICJKV1QifQ==.eyJuYW1lIjogInlpbmdzaGFveG8ifQ==.53c4df02e99e2ce3d3f8d230c799e9f0cbe9963e484b45efe171f38ebe58d690"
    original_dict = jwt_tool.my_jwt_decode(jwt_string=fake_jwt_string, a_secret_string_for_integrity_verifying=secret)
    print(original_dict)