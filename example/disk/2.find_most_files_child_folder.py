# made by baidu ai
import os

def find_folder_with_most_files(parent_folder):
    max_files = 0
    max_folder = ""
    folder_stats = {}

    for root, dirs, files in os.walk(parent_folder):
        file_count = len(files)
        folder_stats[root] = file_count

        if file_count > max_files:
            max_files = file_count
            max_folder = root

    return max_folder, max_files, folder_stats

def print_report(parent_folder, max_folder, max_files, folder_stats):
    print("\nFolder Analysis Report for: {}".format(parent_folder))
    print("="*50)
    print("Total folders scanned: {}".format(len(folder_stats)))
    print("Folder with most files: {}".format(max_folder))
    print("Number of files: {}".format(max_files))
    print("\nTop 10 folders by file count:")
    print("-"*30)

    sorted_folders = sorted(folder_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    for folder, count in sorted_folders:
        print("{}: {} files".format(folder, count))

if __name__ == "__main__":
    #parent_folder = raw_input("Enter parent folder path: ")
    parent_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code/"
    #parent_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code_Mini/"

    if not os.path.exists(parent_folder):
        print("Error: Folder does not exist")
        exit()

    max_folder, max_files, folder_stats = find_folder_with_most_files(parent_folder)
    print_report(parent_folder, max_folder, max_files, folder_stats)
