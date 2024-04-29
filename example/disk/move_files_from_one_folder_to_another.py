from auto_everything.disk import Disk, Store
disk = Disk()
from auto_everything.terminal import Terminal_User_Interface
terminal_user_interface = Terminal_User_Interface()

disk_A_path = "/media/yingshaoxo/yingshaoxo/temp_folder"
disk_B_path = "/media/yingshaoxo/yingshaoxo/Yingshaoxo_Data"

def get_file_and_folder(source_folder_path=None):
    files = disk.get_folder_and_files(folder=source_folder_path)
    data_list = []
    for file_or_folder in files:
        data_list.append({
            "path": file_or_folder.path,
            "type": 'folder' if file_or_folder.is_folder else 'file'
        })
    return data_list

disk_a_file_or_folder_list = get_file_and_folder(disk_A_path)
disk_b_file_or_folder_list = get_file_and_folder(disk_B_path)

print("Disk A files number:", len(disk_a_file_or_folder_list))
print("Disk B files number:", len(disk_b_file_or_folder_list))

def merge_two_dict(dict_a, dict_b):
    dict_c = dict_a.copy()
    dict_c.update(dict_b)
    return dict_c

disk_a_pure_files = [merge_two_dict(one, {"sub_string": one["path"].split(disk_A_path+"/")[-1]}) for one in disk_a_file_or_folder_list]
disk_b_pure_files = [merge_two_dict(one, {"sub_string": one["path"].split(disk_B_path+"/")[-1]}) for one in disk_b_file_or_folder_list]

for file_a in disk_a_pure_files:
    try:
        full_path = file_a["path"]
        sub_path = file_a["sub_string"]
        target_path = disk.join_paths(disk_B_path, sub_path)

        if file_a["type"] == "folder":
            continue

        if not disk.exists(target_path):
            parent_folder = disk.get_parent_directory_path(target_path)
            disk.create_a_folder(parent_folder)

            disk.move_a_file(full_path, target_path)
        else:
            if disk.get_file_size(full_path) != disk.get_file_size(target_path):
                parent_folder = disk.get_parent_directory_path(target_path)
                disk.create_a_folder(parent_folder)

                disk.move_a_file(full_path, target_path)
    except Exception as e:
        print(e)

print("done")
