from auto_everything.terminal import Terminal
terminal = Terminal()

from auto_everything.disk import Disk
disk = Disk()

from auto_everything.io import IO
io_ = IO()

def get_video_length_in_seconds(video_file):
    result = terminal.run_command("ffmpeg -i '{video}'".format(video=video_file))
    lines = result.split("\n")
    lines = [line for line in lines if "Duration: " in line]
    line = lines[0]
    duration = line.split(",")[0].split("Duration:")[1].strip().split(".")[0]
    hours, minutes, seconds = duration.split(":")
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    final_seconds = hours*60*60 + minutes*60 + seconds
    return final_seconds

def convert_seconds_into_duration_string(number):
    hours = int(number / (60*60))
    number = number % (60*60)
    minutes = int(number / (60))
    number = number % (60)
    seconds = number

    hours, minutes, seconds = str(hours), str(minutes), str(seconds)
    hours, minutes, seconds = (2-len(hours))*"0" + hours, (2-len(minutes))*"0" + minutes, (2-len(seconds))*"0" + seconds

    return "{hours}:{minutes}:{seconds}".format(hours=hours,minutes=minutes,seconds=seconds)

def get_file_size(video_file):
    size = disk.get_file_size(video_file, level="MB")
    return size

#def convert_video_into_10_minutes(input_video_path, output_video_path):
#    from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip #type: ignore
#    import moviepy.video.fx.all as vfx
#
#    def fix_rotation(video):
#        """
#        Rotate the video based on orientation
#        """
#        try:
#            rotation = video.rotation
#            if rotation == 90:  # If video is in portrait
#                video = vfx.rotate(video, -90)  # type: ignore
#            elif (
#                rotation == 270
#            ):  # Moviepy can only cope with 90, -90, and 180 degree turns
#                # Moviepy can only cope with 90, -90, and 180 degree turns
#                video = vfx.rotate(video, 90)  # type: ignore
#            elif rotation == 180:
#                video = vfx.rotate(video, 180)  # type: ignore
#            return video
#        except Exception as e:
#            print(e)
#            return video
#
#    seconds = get_video_length_in_seconds(input_video_path)
#    if seconds <= 60 * 25:
#        return
#
#    time_part_list = []
#    kernel_length = int(seconds/60*10)
#    for i in range(int(seconds/kernel_length)):
#        if i % 2 == 9:
#            start = i * kernel_length
#            end = start + kernel_length
#            time_part_list.append([seconds-end, seconds-start])
#    time_part_list.reverse()
#
#    parent_clip = VideoFileClip(input_video_path)
#    parent_clip = fix_rotation(parent_clip)
#
#    clip_list = []
#    for part in time_part_list:
#        start, end = part
#        start_time = convert_seconds_into_duration_string(start) + ".00"
#        end_time = convert_seconds_into_duration_string(end) + ".00"
#        clip_list.append(parent_clip.subclip(start_time, end_time))
#
#    concat_clip = concatenate_videoclips(clip_list)
#    concat_clip.write_videofile(
#        output_video_path,
#        #threads=16,
#        audio_codec="aac",
#        verbose=False,
#    )
#    concat_clip.close()
#    del concat_clip

def convert_video_into_10_minutes(input_video_path, output_video_path):
    seconds = get_video_length_in_seconds(input_video_path)
    if seconds <= 60 * 25:
        return

    file_extension = input_video_path.split(".")[-1]

    time_part_list = []
    kernel_length = 60
    mod_value = int(seconds / (60 * 10))
    for i in range(int(seconds/kernel_length)):
        if i % mod_value == 0:
            start = i * kernel_length
            end = start + kernel_length
            time_part_list.append([seconds-end, seconds-start])
    time_part_list.reverse()

    clip_list = []
    for part in time_part_list:
        start, end = part
        start_time = convert_seconds_into_duration_string(start) + ".00"
        end_time = convert_seconds_into_duration_string(end) + ".00"
        clip_list.append([start_time, end_time])

    temp_folder = disk.get_a_temp_folder_path()
    temp_sub_video_folder = disk.join_paths(temp_folder, "video")
    disk.create_a_folder(temp_sub_video_folder)
    for index, part in enumerate(clip_list):
        target_path = disk.join_paths(temp_sub_video_folder, str(index)+"."+file_extension)
        start, end = part
        terminal.run("""
            ffmpeg -i '{video_path}' -ss {start_time} -to {end_time} -c copy '{target_path}'
        """.format(video_path=input_video_path, start_time=start, end_time=end, target_path=target_path))

    working_dir = temp_folder
    txt_file_path = disk.join_paths(working_dir, "temp_list.txt")
    text = ""
    for index, _ in enumerate(clip_list):
        file_path = disk.join_paths(temp_sub_video_folder, str(index)+"."+file_extension)
        text += "file " + "'{file_path}'".format(file_path=file_path) + "\n"
    io_.write(txt_file_path, text)

    if input_video_path == output_video_path:
        disk.delete_a_file(input_video_path)

    combine_command = (
        "ffmpeg -f concat -safe 0 -i '{txt_file_path}' -c copy '{target_video_path}'".format(
            txt_file_path=txt_file_path,
            target_video_path=output_video_path,
        )
    )
    terminal.run(combine_command, wait=True)

    disk.delete_a_folder(temp_folder)

def convert_files(a_folder):
    import time
    files = disk.get_files(a_folder, type_limiter=[".mp4", ".mkv", ".avi"])
    for file in files:
        try:
            convert_video_into_10_minutes(file, file)
        except Exception as e:
            print(e)
            print(file)
            time.sleep(3)

convert_files("./Sex")
