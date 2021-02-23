from auto_everything.video import Video

video = Video()
video.humanly_remove_silence_parts_from_video(source_video_path="/home/yingshaoxo/Videos/demo.mp4", target_video_path="/home/yingshaoxo/Videos/final.mp4", db_for_split_silence_and_voice=25)
