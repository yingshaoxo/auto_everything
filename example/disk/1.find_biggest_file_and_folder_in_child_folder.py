# made by baidu ai
import os
from heapq import nlargest

def get_folder_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except (OSError, IOError):
                continue
    return total

def format_size(size_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units)-1:
        size_bytes /= 1024
        unit_index += 1
    return "{:.2f} {}".format(size_bytes, units[unit_index])

def analyze_storage(parent_folder):
    file_sizes = []
    folder_sizes = []

    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_sizes.append((file_path, file_size))
            except (OSError, IOError):
                continue

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                dir_size = get_folder_size(dir_path)
                folder_sizes.append((dir_path, dir_size))
            except (OSError, IOError):
                continue

    top_files = nlargest(20, file_sizes, key=lambda x: x[1])
    top_folders = nlargest(20, folder_sizes, key=lambda x: x[1])
    return top_files, top_folders

def print_report(parent_folder, top_files, top_folders):
    print("\nStorage Analysis Report for: {}".format(parent_folder))
    print("="*70)

    print("\nTop 20 Largest Files:")
    print("-"*30)
    for i, (path, size) in enumerate(top_files, 1):
        print("{}. {} ({})".format(i, path, format_size(size)))

    print("\nTop 20 Largest Folders:")
    print("-"*30)
    for i, (path, size) in enumerate(top_folders, 1):
        print("{}. {} ({})".format(i, path, format_size(size)))

if __name__ == "__main__":
    #parent_folder = raw_input("Enter parent folder path: ").strip()
    parent_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code/"
    if not os.path.exists(parent_folder):
        print("Error: Folder does not exist")
        exit()

    top_files, top_folders = analyze_storage(parent_folder)
    print_report(parent_folder, top_files, top_folders)
