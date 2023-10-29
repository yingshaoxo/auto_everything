from auto_everything.disk import Disk

disk = Disk()
files = disk.get_files("~/CS/auto_everything", recursive=True, use_gitignore_file=True)

for file in files:
    print(file)
