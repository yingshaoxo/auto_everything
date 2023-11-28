from auto_everything.disk import Disk
disk = Disk()
from pydub import AudioSegment

input_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Music/一只怪兽叭"
output_mp3_file = disk._expand_user("~/Downloads/one.mp3")

if not disk.exists(input_folder):
    print(f"You have to give me a right mp3 input folder than '{input_folder}'")
    exit()

files = disk.get_files(input_folder, type_limiter=[".mp3"])

sound = None
for index, file in enumerate(files):
    print("Processing:", file)
    if index == 0:
        sound = AudioSegment.from_mp3(file)
        continue
    sound = sound.append(AudioSegment.silent(duration=10000))#, crossfade=1500)
    sound = sound.append(AudioSegment.from_mp3(file))#, crossfade=1500)

sound.export(output_mp3_file, format="mp3")
print("Done.")
print(f"You can check the output mp3 file in '{output_mp3_file}'")
