from auto_everything.disk import Disk

disk = Disk()
#root_node = disk.get_folder_and_files_tree("~/CS/auto_everything", True)
root_node = disk.get_folder_and_files_with_gitignore("~/CS/style_shop", True, True)

queue = [root_node]
while len(queue) > 0:
    node = queue[0]
    queue = queue[1:]
    if node.children != None:
        queue += node.children
    print(f"folder {node.is_folder}, file {node.is_file}", ":", node.path)
