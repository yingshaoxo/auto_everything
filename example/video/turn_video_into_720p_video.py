from auto_everything.terminal import Terminal
terminal = Terminal()

from auto_everything.disk import Disk
disk = Disk()

def convert_video_into_720p(input_video_path, output_video_path, use_720p=True):
    if use_720p == True:
        resolution = "1280:720"
        kb_limit = "747k"
    else:
        resolution = "1920:1080"
        kb_limit = "1120k"

    #combine_command = """
    #    ffmpeg -i '{video_path}' -c:v libx264 -vf scale={resolution} -r 23.98 -b:v {kb_limit} -c:a copy '{target_path}'
    #""".format(video_path=input_video_path, resolution=resolution, kb_limit=kb_limit, target_path=output_video_path)

    combine_command = """
        ffmpeg -i '{video_path}' -c:v libx264 -vf "scale={resolution}:flags=neighbor" -r 23.98 -b:v {kb_limit} -c:a copy '{target_path}'
    """.format(video_path=input_video_path, resolution=resolution, kb_limit=kb_limit, target_path=output_video_path)

    terminal.run(combine_command, wait=True)

def convert_files(a_folder, use_720p=True):
    import time
    files = disk.get_files(a_folder, type_limiter=[".mp4", ".mkv", ".avi"])
    for file in files:
        try:
            convert_video_into_720p(file, file+"."+file.split(".")[-1], use_720p=use_720p)
        except Exception as e:
            print(e)
            print(file)
            time.sleep(3)

the_folder = "./TV_shows/test"
print(the_folder)
input("Is this folder you want to compress?")

response = input("Convert to 720p input 1, 1080p input 2: ").strip()
if response == "1":
    convert_files(the_folder, True)
elif response == "2":
    convert_files(the_folder, False)
