from auto_everything.disk import Disk
import os

disk = Disk()
files = disk.get_files(".", False, type_limiter=[".png", ".jpg"])
for file in files:
    hash = disk.get_hash_of_a_file(file)
    stem, suffix = disk.get_stem_and_suffix_of_a_file(file)
    print(stem)
    os.rename(file, hash+suffix)
