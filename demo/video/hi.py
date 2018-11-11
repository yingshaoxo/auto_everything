from auto_everything.video import Video

video = Video("/home/yingshaoxo/Videos/doing.mp4")
#video_file_path = video.combine_all_mp4_in_a_folder("/home/yingshaoxo/Videos/doing")
#video.remove_silence_parts_from_video(video_file_path)
video._check_db()
exit()
video.remove_silence_parts_from_video("/home/yingshaoxo/Videos/doing.mp4", db_for_split_silence_and_voice=20)
