from auto_everything.disk import Disk, Store
disk = Disk()
from auto_everything.terminal import Terminal_User_Interface
terminal_user_interface = Terminal_User_Interface()

def encrypt_the_bytes(original_bytes):
    prefix_bytes = bytes(("yingshaoxo_is_the_best"*1).encode("utf-8"))
    return prefix_bytes + original_bytes

def decrypt_the_bytes(encrypted_bytes):
    prefix_bytes = bytes(("yingshaoxo_is_the_best"*1).encode("utf-8"))
    return encrypted_bytes[len(prefix_bytes):]

#file_a = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/1.mp3"
#with open(file_a, "rb") as f:
#    file_bytes = f.read()
#
#new_file_bytes = encrypt_the_bytes(file_bytes)
#file_b = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/2.mp3"
#with open(file_b, "wb") as f:
#    f.write(new_file_bytes)
#
#file_c = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/3.mp3"
#with open(file_c, "wb") as f:
#    f.write(decrypt_the_bytes(new_file_bytes))

def encrypt_a_folder(from_folder, to_folder):
    files = disk.get_folder_and_files(folder=from_folder)
    data_list = []
    for file_or_folder in files:
        if file_or_folder.is_folder:
            # create a folder
            try:
                new_end_path = file_or_folder.path[len(from_folder):]
                new_end_path = to_folder + new_end_path
                disk.create_a_folder(new_end_path)
            except Exception as e:
                print(e)
        else:
            # file_or_folder.path
            with open(file_or_folder.path, "rb") as f:
                old_bytes = f.read()
            new_bytes = encrypt_the_bytes(old_bytes)

            new_end_path = file_or_folder.path[len(from_folder):]
            new_end_path = to_folder + new_end_path
            with open(new_end_path, "wb") as f:
                f.write(new_bytes)

def decrypt_a_folder(from_folder, to_folder):
    files = disk.get_folder_and_files(folder=from_folder)
    data_list = []
    for file_or_folder in files:
        if file_or_folder.is_folder:
            # create a folder
            try:
                new_end_path = file_or_folder.path[len(from_folder):]
                new_end_path = to_folder + new_end_path
                disk.create_a_folder(new_end_path)
            except Exception as e:
                print(e)
        else:
            # file_or_folder.path
            with open(file_or_folder.path, "rb") as f:
                old_bytes = f.read()
            new_bytes = decrypt_the_bytes(old_bytes)

            new_end_path = file_or_folder.path[len(from_folder):]
            new_end_path = to_folder + new_end_path
            with open(new_end_path, "wb") as f:
                f.write(new_bytes)

disk_A_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Videos"
disk_B_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Videos_encrypted_by_adding_a_string_at_beginning"
disk_C_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/test3"

encrypt_a_folder(disk_A_path, disk_B_path)
#decrypt_a_folder(disk_B_path, disk_C_path)









"""
# method 2

def encrypt_the_byte_int(a_number):
    a_number = a_number + 1
    if a_number > 255:
        a_number = 0
    return a_number

def decrypt_the_byte_int(a_number):
    a_number = a_number - 1
    if a_number < 0:
        a_number = 255
    return a_number


file_a = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/1.mp4"
file_b = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/2.mp4"
file_c = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/3.mp4"
file_stream_1 = open(file_a, "rb")
file_stream_2 = open(file_b, "ab")
file_stream_3 = open(file_c, "ab")

byte = file_stream_1.read(1)
while byte:
    int_byte = byte[0]

    new_int = encrypt_the_byte_int(int_byte)
    new_byte = bytes([new_int])
    file_stream_2.write(new_byte)

    recover_byte = decrypt_the_byte_int(new_int)
    file_stream_3.write(new_byte)

    byte = file_stream_1.read(1)

file_stream_1.close()
file_stream_2.close()
file_stream_3.close()

exit()
"""
