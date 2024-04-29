"""
We find node_modules simply because it takes space and there are too much useless files, for example, 5000 packages * 500 files.

But there also have chances some project in your git host does not have the right .gitignore file.

In the end, for some game project, they may used big media file without warning you. For example, they use a 25MB wav audio file that only has 1 minute sound. Which is not right, because 1 minute 64kps sound in mp3 format will only take less than 500KB storage. And for pictures, 480p image will only take less than 200KB storage.
"""
import os

from auto_everything.disk import Disk, Store
disk = Disk()
store = Store("disk_sync_example")
store2 = Store("disk_check")
from auto_everything.terminal import Terminal_User_Interface
terminal_user_interface = Terminal_User_Interface()

disk_a_file_or_folder_list = store.get("disk_a_list", [])

if disk_a_file_or_folder_list == []:
    print("no file is inside of " + disk_A_path)
    exit()

print("Disk A files number:", len(disk_a_file_or_folder_list))


input("I suggest you to use 'python3 ./example/terminal/Tools.py find_big_file_and_folders to find big folder'")


reply = terminal_user_interface.selection_box(text="-1. find node_modules?", selections=["no", "yes"])
if "yes" in reply:
    root_folder_set = set()
    for file in disk_a_file_or_folder_list:
        full_path = file["path"]

        if file["type"] == "folder":
            if full_path.strip("/").endswith("node_modules"):
                if disk.exists(full_path):
                    print(full_path)


reply = terminal_user_interface.selection_box(text="0. get folder and its children:", selections=["no", "yes"])
if "yes" in reply:
    folder_path_to_sub_child_dict = {}
    # key is full folder path, value is first level child folder name list

    root_folder_set = set()
    for file in disk_a_file_or_folder_list:
        full_path = file["path"]

        if file["type"] == "folder":
            if disk.exists(full_path):
                sub_folder_and_files = os.listdir(full_path)
                children_number = len(sub_folder_and_files)
                if children_number == 0:
                    parent_level_3_folder = "/".join(full_path.split("/")[:-1])
                    root_folder_set.add(parent_level_3_folder)

    for folder in root_folder_set:
        children = disk.get_files(folder)
        children_number = len(children)
        if children_number >= 300:
            folder_path_to_sub_child_dict[folder] = children_number
            print(folder + ":", children_number)

    store2.set("folder_and_its_children", folder_path_to_sub_child_dict)
    #check children in recursive way

