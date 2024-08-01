from pprint import pprint
from auto_everything.disk import Disk
disk = Disk()

input_folder = "~/CS/style_shop"

files1 = disk.get_gitignore_folders_and_files_by_using_yingshaoxo_method(input_folder, also_return_dot_git_folder=False)
files2 = disk.get_gitignore_folders_and_files(input_folder)

print(files1)
print(files2)

input("\nDo you want to get files and folders without ignored files or folders?")
files3 = disk.get_folder_and_files_with_gitignore(input_folder, return_list_than_tree=True)
for one in files3:
    print(one.path)

"""
root_node = disk.get_folder_and_files_with_gitignore(input_folder, return_list_than_tree=False)
queue = [root_node]
while len(queue) > 0:
    node = queue[0]
    queue = queue[1:]
    if node.children != None:
        queue += node.children
    print(f"folder {node.is_folder}, file {node.is_file}", ":", node.path)
"""
