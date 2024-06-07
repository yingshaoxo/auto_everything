from auto_everything.video_ import Video
video = Video()

def image_handler(a_image):
    return a_image.get_simplified_image_in_a_quick_way(level=15)

def audio_handler(a_audio):
    return a_audio
    #return a_audio.get_extreme_simplified_audio(max_signal_value=9)

video.video_to_video(source_video_path="/home/yingshaoxo/Downloads/naruto_small.mp4", target_video_path="/home/yingshaoxo/Downloads/naruto_output.mp4", image_handler=image_handler, audio_handler=audio_handler, temp_folder="/home/yingshaoxo/Downloads/temp")
