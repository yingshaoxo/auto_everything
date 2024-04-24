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

disk_A_path = "/home/yingshaoxo/CS/auto_everything"
disk_B_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data"

def fake_storage_backup(source_folder_path=None):
    files = disk.get_folder_and_files_with_gitignore(folder=source_folder_path, return_list_than_tree=True)
    data_list = []
    for file_or_folder in files:
        print("ok")
        data_list.append({
            "path": file_or_folder.path,
            "type": 'folder' if file_or_folder.is_folder else 'file'
        })
    return data_list

disk_a_file_or_folder_list = fake_storage_backup(disk_A_path)
print(disk_a_file_or_folder_list)

#result = terminal_user_interface.selection_box(text="Please select one:", selections=["a", "b"])
#print(result)

