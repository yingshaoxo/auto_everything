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


class Simple_Video():
    def split_video_to_images_and_audio(self):
        """
        For example, "hi.mp4", have 3 seconds length of data
        it will be in a "hi" folder, inside of hi folder, there should have "images" folder and "audio.wav" file
        in the "images" folder, there should have ["1", "2", "3"] 3 folders to represente 3 seconds
        in each seconds folder, there should have 20 pictures from "1.png" to "20.png". (but it could have just have 2 images, which means 1 second only have to images)
        """
        pass

    def merge_images_and_audio_to_video(self):
        """
        For example, "hi.mp4", have 3 seconds length of data
        it will be in a "hi" folder, inside of hi folder, there should have "images" folder and "audio.wav" file
        in the "images" folder, there should have ["1", "2", "3"] 3 folders to represente 3 seconds
        in each seconds folder, there should have 20 pictures from "1.png" to "20.png". (but it could have just have 2 images, which means 1 second only have to images)
        """
        pass

    def read_video_from_file(self):
        # if it is a folder, we read our own data structure
        pass

    def write_video_to_file(self):
        # if it is a folder, we write our own data structure
        pass
