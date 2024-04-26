"""
How to sync data in 3 disk storage?

1. You have diskA, diskB, and diskC. diskC should have biggest storage.
2. You compare diskA, diskB and diskC, find common things in 3 disk. find different parts in 3 disk.
3. You manually choose what folder or file in diskA need to get saved. A software will remember that.
4. You manually choose what folder or file in diskB need to get saved. This time it would be easier for you because software remembers some choice you did last time.
5. You copy everything need to get saved from diskA and diskB to diskC.
6. You delete unwanted difference data in diskC.
7. You re-manage diskC data.
8. You copy diskC data into diskA and diskB directly by overwrite everything.
"""

from auto_everything.disk import Disk, Store
disk = Disk()
store = Store("disk_sync_example")
from auto_everything.terminal import Terminal_User_Interface
terminal_user_interface = Terminal_User_Interface()

disk_A_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data"
disk_B_path = "/media/yingshaoxo/yingshaoxo/Yingshaoxo_Data"
common_part = "/Yingshaoxo_Data/"
temp_folder = "/media/yingshaoxo/yingshaoxo/temp_folder"

def get_file_and_folder_with_gitignore(source_folder_path=None):
    files = disk.get_folder_and_files_with_gitignore(folder=source_folder_path, return_list_than_tree=True)
    data_list = []
    for file_or_folder in files:
        data_list.append({
            "path": file_or_folder.path,
            "type": 'folder' if file_or_folder.is_folder else 'file'
        })
    return data_list

def get_file_and_folder(source_folder_path=None):
    files = disk.get_folder_and_files(folder=source_folder_path)
    data_list = []
    for file_or_folder in files:
        data_list.append({
            "path": file_or_folder.path,
            "type": 'folder' if file_or_folder.is_folder else 'file'
        })
    return data_list

### 0 scan disk
reply = terminal_user_interface.selection_box(text="0. Do you want to scan disk:", selections=["no", "yes"])
if "yes" in reply:
    ### 1 scan disk a
    reply = terminal_user_interface.selection_box(text="1. Do you want to scan disk A again:", selections=["no", "yes"])
    if "yes" in reply:
        disk_a_file_or_folder_list = get_file_and_folder_with_gitignore(disk_A_path)
        store.set("disk_a_list", disk_a_file_or_folder_list)
    else:
        disk_a_file_or_folder_list = store.get("disk_a_list", [])

    ### 2 scan disk b
    reply = terminal_user_interface.selection_box(text="1. Do you want to scan disk B again:", selections=["no", "yes"])
    if "yes" in reply:
        disk_b_file_or_folder_list = get_file_and_folder(disk_B_path)
        store.set("disk_b_list", disk_b_file_or_folder_list)
    else:
        disk_b_file_or_folder_list = store.get("disk_b_list", [])

    ### 3 get common part
    def merge_two_dict(dict_a, dict_b):
        dict_c = dict_a.copy()
        dict_c.update(dict_b)
        return dict_c

    disk_a_pure_files = [merge_two_dict(one, {"sub_string": one["path"].split(common_part)[-1]}) for one in disk_a_file_or_folder_list]
    store.set("disk_a_list", disk_a_pure_files)
    disk_b_pure_files = [merge_two_dict(one, {"sub_string": one["path"].split(common_part)[-1]}) for one in disk_b_file_or_folder_list]
    store.set("disk_b_list", disk_b_pure_files)

disk_a_file_or_folder_list = store.get("disk_a_list", [])
if disk_a_file_or_folder_list == []:
    print("no file is inside of " + disk_A_path)
    exit()

disk_b_file_or_folder_list = store.get("disk_b_list", [])
if disk_b_file_or_folder_list == []:
    print("no file is inside of " + disk_B_path)
    exit()

print("Disk A files number:", len(disk_a_file_or_folder_list))
print("Disk B files number:", len(disk_b_file_or_folder_list))

def convert_to_text(a_list):
    text = ""
    for file in a_list:
        text += file["sub_string"] + "\n"
    return "\n"+text

disk_a_text_backup = convert_to_text(disk_a_file_or_folder_list)
disk_b_text_backup = convert_to_text(disk_b_file_or_folder_list)

def handle_file_in_disk_b_but_not_in_disk_a():
    disk_a_text = disk_a_text_backup
    disk_b_text = disk_b_text_backup

    folder_that_in_disk_b_but_not_in_disk_a = []
    file_that_in_disk_b_but_not_in_disk_a = []
    for file_b in disk_b_file_or_folder_list:
        full_path = file_b["path"]
        file_b_sub_string = file_b["sub_string"]

        if ("\n"+file_b_sub_string + "\n") not in disk_a_text:
            if file_b["type"] == "folder":
                folder_that_in_disk_b_but_not_in_disk_a.append(file_b)
                target_path = disk.join_paths(temp_folder, file_b_sub_string)
                disk.create_a_folder(target_path)
            else:
                file_that_in_disk_b_but_not_in_disk_a.append(file_b)
            print(file_b_sub_string)

        disk_a_text = disk_a_text.replace("\n"+file_b_sub_string + "\n", "\n")

    for one in file_that_in_disk_b_but_not_in_disk_a:
        try:
            full_path = one["path"]
            sub_path = one["sub_string"]
            target_path = disk.join_paths(temp_folder, sub_path)

            parent_folder = disk.get_parent_directory_path(target_path)
            disk.create_a_folder(parent_folder)

            disk.move_a_file(full_path, target_path)
        except Exception as e:
            print(e)

    print("done")

reply = terminal_user_interface.selection_box(text="2. Do you want to handle_file_in_disk_b_but_not_in_disk_a:", selections=["no", "yes"])
if "yes" in reply:
    handle_file_in_disk_b_but_not_in_disk_a()

def copy_disk_a_data_into_disk_b_by_check_size():
    disk_a_text = disk_a_text_backup
    disk_b_text = disk_b_text_backup

    for file_a in disk_a_file_or_folder_list:
        file_a_sub_string = file_a["sub_string"]
        full_path = file_a["path"]
        sub_path = file_a["sub_string"]
        target_path = disk.join_paths(disk_B_path, sub_path)

        if ("\n" + file_a_sub_string + "\n") not in disk_b_text:
            # directly copy
            if file_a["type"] == "folder":
                disk.create_a_folder(target_path)
            else:
                parent_folder = disk.get_parent_directory_path(target_path)
                disk.create_a_folder(parent_folder)

                disk.copy_a_file(full_path, target_path)
        else:
            # check size, if size not match, replace disk b with disk a data
            if file_a["type"] != "folder":
                if disk.get_file_size(full_path) != disk.get_file_size(target_path):
                    parent_folder = disk.get_parent_directory_path(target_path)
                    disk.create_a_folder(parent_folder)

                    disk.copy_a_file(full_path, target_path)

        disk_b_text = disk_b_text.replace("\n" + file_a_sub_string + "\n", "\n")

    print("done")

reply = terminal_user_interface.selection_box(text="3. Do you want to copy_disk_a_data_into_disk_b:", selections=["no", "yes"])
if "yes" in reply:
    copy_disk_a_data_into_disk_b_by_check_size()
