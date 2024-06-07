"""
The video first can be split into images(pictures) and audio.

Normally, one second 20 images would be enough. For each image, it should not be a complete image, but the changed part of previous image. So that the over all images size can get reduced.

I think for reduce the risks of lossing data in disk and considering the video stream needs, we'd better to split a video into 10 minutes length smaller video list. In other words, a 120 minutes movie can be split into 12 smaller videos.

As for the compression algorithm, the head line should have the information about the image width and height.

After that, first, it should have a rgb color dict, where key is rgb data, value is the index. The index process should make sure the most frequent grb value has the smallest number as index.

Then save the real image matrix data by using index and space symbol. For example: "0 0 1 1 0 1". For each new line of pixels, we still use new line to do the seperation. (Here you can use index_to_rgb dict to get real rgb matrix data, or 2d array where each point is [r,g,b])

If a index has repetition in the right direction in the same row, we use underline with the repetition number to indicate that, for example, if index 2 repeated 200 times, then we write it as "2_200".

If a index takes the whole line, we represente it as "2_d_1". It means the index 2 takes the whole line and repeated its line in the down direction for 1 times.

If a index takes the whole line and repeated its line for 300 times, we represente it as "22_d_300". It means the index 22 takes the whole line and repeated its line in the down direction for 300 times.

In a overview looking, the video should be a folder where the images file and audio file should have same name. For example, a video called "hi_you.mkv", it should end up with a folder called "hi_you", inside of that folder, it should have "hi_you_1.mkv.txt", "hi_you_2.mkv.txt", "hi_you_1.wav.txt", "hi_you_2.wav.txt"

mkv is better since you can play it in a stream way on internet, while mp4 requires you fully download before you can play it.

But any way, in the end all other format is not reliable, you have to save data with your own format.



Let me talk more about the video compression:

Video is special, it is composed by a list of continuse images. By only record the changed part of next image compared to previous image is not enough, we need to do more compression. For example, for each 30x30 pixel square sub_image, we can reuse it in later data representation. It is like you have a sub_image dict pre_loaded, for each image you have later, you generate that image by using dict sub_image_id. For each image, you treat it like a canvas, you draw rectangle or any other shape on it. I did not metion the svg format yet, but similarly, you can use math description to represent a shape, for example, a circle will only require a center point and radius, but if you use pixels, that would be a really huge data.

And for svg, the highest level of data compression algorithm is graphic user interface making, UI engine or game engine. Just think, if you record a website changeable view, how many storage it would take? But actually it is just html+css+js code and a broswer decoder. Or if you think about a 3D game, how many disk space you will use for recording every aspect of that game? But the game itself is small. (Currently public 3D game engine is garbage, it can't produce high quality image or video as 2D game engine would do. A general 2D game engine is UI engine, programmers who uses UI engine are called front-end developers.)

For some video type, for example, porn, you can even loop video segments to reduce size. For animation, 3D to 2D, you have to "reduce shadow color", darker white to white, darker red to red.



author: yingshaoxo
"""

import multiprocessing
from time import sleep

from auto_everything.terminal import Terminal
from auto_everything.disk import Disk
from auto_everything.audio_ import Audio
from auto_everything.image_ import Image
terminal = Terminal()
disk = Disk()


class Video():
    def split_video_to_images_and_audio(self, video_path, output_folder, frame_rate="25", image_format="bmp"):
        """
        This function returns [image_folder, audio_path]

        For example, "hi.mp4", have 3 seconds length of data
        it will be in a "hi" folder, inside of hi folder, there should have "images" folder and "audio.wav" file
        in the "images" folder, there should have ["1", "2", "3"] 3 folders to represente 3 seconds
        in each seconds folder, there should have 25 pictures from "1.png" to "20.png". (but it could have just have 2 images, which means 1 second only have one image)
        """
        image_folder = disk.join_paths(output_folder, "images")
        audio_path = disk.join_paths(output_folder, "audio.wav")

        terminal.run(f"""
            mkdir '{output_folder}'
        """)

        terminal.run(f"""
            rm -fr '{audio_path}'
            ffmpeg -i '{video_path}' '{audio_path}'
        """)

        image_folder = image_folder.rstrip("/")
        frame_rate = str(frame_rate)
        terminal.run(f"""
            rm -fr '{image_folder}'
            mkdir '{image_folder}'
            ffmpeg -i '{video_path}' -r {frame_rate} '{image_folder}/%d.{image_format}'
        """)

        return image_folder, audio_path

    def merge_images_and_audio_to_video(self, image_folder, audio_path, video_path, frame_rate="25", image_format="bmp", video_kb_limit=None):
        """
        For example, "hi.mp4", have 3 seconds length of data
        it will be in a "hi" folder, inside of hi folder, there should have "images" folder and "audio.wav" file
        in the "images" folder, there should have ["1", "2", "3"] 3 folders to represente 3 seconds
        in each seconds folder, there should have 20 pictures from "1.png" to "20.png". (but it could have just have 2 images, which means 1 second only have to images)
        """
        image_folder = image_folder.rstrip("/")

        temp_target_video_path = disk.get_a_temp_file_path("tempvideo.mp4")
        if video_kb_limit == None:
            terminal.run(f"""
                rm -fr '{temp_target_video_path}'
                ffmpeg -framerate {frame_rate} -i '{image_folder}/%d.{image_format}' '{temp_target_video_path}'
            """)
        else:
            terminal.run(f"""
                rm -fr '{temp_target_video_path}'
                ffmpeg -framerate {frame_rate} -i '{image_folder}/%d.{image_format}' -b:v {video_kb_limit}k '{temp_target_video_path}'
            """)

        terminal.run(f"""
            rm -fr '{video_path}'
            ffmpeg -i '{temp_target_video_path}' -i '{audio_path}' -c:v copy -c:a aac -b:a 64k '{video_path}'
        """)

        terminal.run(f"""
            rm -fr '{temp_target_video_path}'
        """)

        return video_path

    def read_video_from_file(self):
        # if it is a folder, we read our own data structure
        pass

    def write_video_to_file(self):
        # if it is a folder, we write our own data structure
        pass

    def video_to_video(self, source_video_path, target_video_path, image_handler=None, audio_handler=None, temp_folder=None):
        if image_handler == None and audio_handler == None:
            disk.copy_a_file(source_video_path, target_video_path)
            return

        def get_black_image_for_error_frame(a_image):
            height, width = a_image.get_shape()
            for y in range(height):
                for x in range(width):
                    a_image.raw_data[y][x] = [0, 0, 0, 255]
            return a_image

        def handle_an_image_in_another_process(image_path):
            a_image = Image().read_image_from_file(image_path)
            try:
                a_image = image_handler(a_image)
            except Exception as e:
                print(e)
                a_image = get_black_image_for_error_frame(a_image)
            a_image.save_image_to_file_path(image_path.split(".")[0] + ".png")

        cpu_number = multiprocessing.cpu_count() * 2

        video_info = terminal.run_command(f"ffmpeg -i '{source_video_path}'")
        lines = [line for line in video_info.split("\n") if " fps" in line]
        frame_rate = "25"
        kb_per_second = None
        if len(lines) != 0:
            line = lines[0]
            info_list = line.split(",")
            for info in info_list:
                info = info.strip()
                if " fps" in info:
                    frame_rate = info.split(" fps")[0]
                elif " kb/s" in info:
                    kb_per_second = info.split(" kb/s")[0]

        if temp_folder == None:
            a_temp_folder = disk.get_a_temp_folder_path()
        else:
            a_temp_folder = temp_folder
        image_folder, audio_path = self.split_video_to_images_and_audio(source_video_path, a_temp_folder, image_format="bmp", frame_rate=frame_rate)
        if image_handler == None and audio_handler != None:
            # do process for audio
            a_audio = Audio().read_wav_file(audio_path)
            a_audio = audio_handler(a_audio)
            a_audio.write_wav_file(audio_path)
            print("audio processed.")
        elif image_handler != None and audio_handler == None:
            # do process for image
            images = disk.get_files(image_folder, recursive=False, type_limiter=[".bmp"])
            process_list = []
            counting = 0
            for image_path in images:
                a_process = multiprocessing.Process(target=handle_an_image_in_another_process, args=(image_path,))
                process_list.append(a_process)
                a_process.start()
                if len(process_list) == cpu_number:
                    while True:
                        if any([not one.is_alive() for one in process_list]):
                            break
                        sleep(1)
                    process_list = [one for one in process_list if one.is_alive()]
                counting += 1
                print("image " + str(counting) + " processed.")
            while any([one.is_alive() for one in process_list]):
                sleep(1)
        elif image_handler != None and audio_handler != None:
            # do process for all
            a_audio = Audio().read_wav_file(audio_path)
            a_audio = audio_handler(a_audio)
            a_audio.write_wav_file(audio_path)
            print("audio processed.")

            images = disk.get_files(image_folder, recursive=False)
            process_list = []
            counting = 0
            for image_path in images:
                a_process = multiprocessing.Process(target=handle_an_image_in_another_process, args=(image_path,))
                process_list.append(a_process)
                a_process.start()
                if len(process_list) == cpu_number:
                    while True:
                        if any([not one.is_alive() for one in process_list]):
                            break
                        sleep(1)
                    process_list = [one for one in process_list if one.is_alive()]
                counting += 1
                print("image " + str(counting) + " processed.")
            while any([one.is_alive() for one in process_list]):
                sleep(1)

        terminal.run(f"""
            rm -fr '{image_folder}/*.bmp'
        """)
        video_path = self.merge_images_and_audio_to_video(image_folder, audio_path, target_video_path, frame_rate=frame_rate, image_format="png", video_kb_limit=kb_per_second)
        terminal.run(f"""
            rm -fr '{a_temp_folder}'
        """)
        return video_path
