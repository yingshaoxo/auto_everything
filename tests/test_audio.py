from auto_everything.audio import DeepAudio
deep_audio = DeepAudio()

from auto_everything.video import Video
video = Video()

from auto_everything.disk import Disk
disk = Disk()

from auto_everything.terminal import Terminal
t = Terminal()

import os

def test_speech_enhancement():
    source_video_path = "/Users/yingshaoxo/Movies/Videos/doing.mkv"
    target_video_path = "/Users/yingshaoxo/Movies/Videos/done_speech_enhancement.mp4"

    temp_audio_path = disk.get_a_temp_file_path(disk.get_hash_of_a_path(source_video_path) + "_temp_audio.wav")
    base_name, suffix = disk.get_stem_and_suffix_of_a_file(target_video_path)
    target_audio_path = disk.join_paths(disk.get_directory_name(target_video_path), base_name + ".wav") 

    video.get_wav_from_video(source_video_path=source_video_path, target_audio_path=temp_audio_path, rate=48000)


    current_working_directory = t.run_command("pwd")
    os.chdir("/tmp")
    deep_audio.speech_enhancement_with_speechbrain(
        source_audio_path=temp_audio_path,
        target_audio_path=target_audio_path
    )
    os.chdir(current_working_directory)

    video.replace_old_audio_with_new_wav_file_for_a_video(
        source_video_path=source_video_path, 
        new_wav_audio_path=target_audio_path, 
        target_video_path=target_video_path
    )

    disk.remove_a_file(temp_audio_path)
    disk.remove_a_file(target_audio_path)

    assert disk.exists(target_video_path)


def test_deepFilterNet():
    source_video_path = "/Users/yingshaoxo/Movies/Videos/doing.mkv"
    target_video_path = "/Users/yingshaoxo/Movies/Videos/done_speech_deepFilterNet.mp4"

    temp_audio_path = disk.get_a_temp_file_path(disk.get_hash_of_a_path(source_video_path) + "_temp_audio.wav")
    base_name, suffix = disk.get_stem_and_suffix_of_a_file(target_video_path)
    target_audio_path = disk.join_paths(disk.get_directory_name(target_video_path), base_name + ".wav") 

    video.get_wav_from_video(source_video_path=source_video_path, target_audio_path=temp_audio_path, rate=48000)


    current_working_directory = t.run_command("pwd")
    os.chdir("/tmp")
    deep_audio.speech_enhancement_with_deepFilterNet(
        source_audio_path=temp_audio_path,
        target_audio_path=target_audio_path
    )
    os.chdir(current_working_directory)

    video.replace_old_audio_with_new_wav_file_for_a_video(
        source_video_path=source_video_path, 
        new_wav_audio_path=target_audio_path, 
        target_video_path=target_video_path
    )

    disk.remove_a_file(temp_audio_path)
    disk.remove_a_file(target_audio_path)

    assert disk.exists(target_video_path)