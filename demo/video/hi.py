from auto_everything.video import Video

video = Video("/home/yingshaoxo/Videos/demo.mp4")
video.humanly_remove_silence_parts_from_video(db_for_split_silence_and_voice=20)

#video = Video()
#video_file_path = video.combine_all_mp4_in_a_folder("/home/yingshaoxo/Videos/doing")
