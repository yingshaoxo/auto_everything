# This is a will_loss_information method, do not recommand for high standard information saving

"""
1. first, for those folders and files inside .gitignore, you should not save
2. save .gitgnore
3. only leave [.txt, .md, .py, .c, .cpp, .js, .ts, ...], make sure all 'filename.lower()'. And also, you need to keep the folder tree.


anyway, let me first have a list to see what kind of type we have under CS/auto_everything folder

I suggest you first get folders list, then for each folder, you detect if there has .gitignore, if has, do a fileter based on .gitignore first, then your file type filter. And for anyother child folder, you pass the parent .gitignore content to them. And so on and on.
"""

from auto_everything.disk import Disk
disk = Disk()

file_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code/"
target_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code_Mini/"

type_limiter = [".txt", ".midi_txt", ".md", ".py", ".h", ".c", ".cpp", ".js", ".cjs", ".ts", ".vue", ".sh", ".html", ".scss", ".css", ".json", ".proto", ".dart", ".go", ".yaml", ".php", ".rs", ".toml", ".cc", ".yml", ".lua", ".htm", ".vim", ".hero", ".java", ".sql_command", ".kt", ".CPP", ".less", ".cs", ".e"]
type_limiter2 = [one.lower() for one in type_limiter]
type_limiter3 = [one.upper() for one in type_limiter]
files = disk.get_files(file_folder, True, type_limiter=type_limiter + type_limiter2 + type_limiter3)
#files = disk.get_files(file_folder, True)

new_files = []
for file in files:
    if file.endswith(".e"):
        if file.endswith("E_Python.e"):
            new_files.append(file)
        if file.endswith("YSmodel.e"):
            new_files.append(file)
    else:
        new_files.append(file)
files = new_files

file_types = set()
all_file_size = 0 #in kb
for file in files:
    stem, suffix = disk.get_stem_and_suffix_of_a_file(file)
    file_types.add(suffix)
    all_file_size += disk.get_file_size(file, level="KB")

print(file_types)

print("All file size:")
print(all_file_size, "KB")
print(int(all_file_size/1024), "MB")

input("Do you happy for the final file size you got? If so, hit enter to go on, otherwise, ctrl+c")


for file in files:
    file_name = disk.get_file_name(file)
    parent_folder = disk.get_parent_directory_path(file)
    target_parent_folder = target_folder + parent_folder[len(file_folder):]
    target_file_path = target_parent_folder + "/" + file_name
    #print(target_parent_folder)
    print(target_file_path)
    disk.create_a_folder(target_parent_folder)
    disk.copy_a_file(file, target_file_path)
