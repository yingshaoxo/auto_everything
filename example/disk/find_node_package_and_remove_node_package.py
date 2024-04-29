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

