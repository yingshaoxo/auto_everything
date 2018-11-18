from auto_everything.video import Video

video = Video()
#video_file_path = video.combine_all_mp4_in_a_folder("/home/yingshaoxo/Videos/doing")
#video.remove_silence_parts_from_video(video_file_path)

video.remove_silence_parts_from_video("/home/yingshaoxo/Videos/out.mp4", db_for_split_silence_and_voice=50, minimum_interval_time_in_seconds=3)
