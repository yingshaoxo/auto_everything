from auto_everything.cryptography import EncryptionAndDecryption, Password_Generator


def test_password():
    password_generator = Password_Generator(base_secret_string="yingshaoxo")
    password = password_generator.get_password(secret_string_list=["hi"])
    print(password)
    

def test_cryptography():
    encryption_and_decryption = EncryptionAndDecryption()

    a_dict = encryption_and_decryption.get_secret_alphabet_dict("yingshaoxo is the best")
    print(a_dict)

    a_sentence = "Hello, world, I'm yingshaoxo. Here is the test number: 9111108848."

    encrypted_sentence = encryption_and_decryption.encode_message(a_secret_dict=a_dict, message=a_sentence)
    print()
    print(encrypted_sentence)

    decrypted_sentence = encryption_and_decryption.decode_message(a_secret_dict=a_dict, message=encrypted_sentence)
    print(decrypted_sentence)
