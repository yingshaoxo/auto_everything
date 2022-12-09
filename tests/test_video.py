from auto_everything.video import Video, DeepVideo
video = Video()
deep_video = DeepVideo()

from auto_everything.disk import Disk
disk = Disk()

import librosa
import os
os.environ['LIBROSA_DATA_DIR'] = "/tmp"

def test_hi():
    assert "hi" == "hi"

def test_error():
    assert "yes" == "no"

def test_get_voice_and_silence_parts2():
    filename = librosa.ex('trumpet')
    parts = video._get_voice_and_silence_parts_2(source_audio_path=filename, top_db=21, the_maximum_silent_interval_time_in_seconds_you_wish_to_have=1.5)
    print(parts)
    print(len(parts))
    assert len(parts) != 0
    assert len(parts[0]) == 3
    assert type(parts[0][0]) == int
    assert type(parts[0][1]) == str
    assert type(parts[0][2]) == str


def test_remove_silence_parts_from_video_2():
    source_video_path = "/Users/yingshaoxo/Movies/Videos/doing.mkv"
    target_video_path = "/Users/yingshaoxo/Movies/Videos/done.mp4"
    video.remove_silence_parts_from_video_2(
        source_video_path=source_video_path,
        target_video_path=target_video_path,
        db_for_split_silence_and_voice=21,
        the_maximum_silent_interval_time_in_seconds_you_wish_to_have=1.7
    )
    assert disk.exists(target_video_path)


def test_speedup_silence_parts_in_video_2():
    source_video_path = "/Users/yingshaoxo/Movies/Videos/doing.mkv"
    target_video_path = "/Users/yingshaoxo/Movies/Videos/done.mp4"
    video.speedup_silence_parts_in_video_2(
        source_video_path=source_video_path,
        target_video_path=target_video_path,
        db_for_split_silence_and_voice=21,
        speed=30,
        the_maximum_silent_interval_time_in_seconds_you_wish_to_have=0,
        silent_speedup_part=False
    )
    assert disk.exists(target_video_path)


def test_improve_the_quality_of_human_voice_inside_of_a_video():
    source_video_path = "/Users/yingshaoxo/Movies/Videos/doing.mkv"
    target_video_path = "/Users/yingshaoxo/Movies/Videos/done.mp4"
    deep_video.improve_the_quality_of_human_voice_inside_of_a_video(
        source_video_path=source_video_path,
        target_video_path=target_video_path,
        sample_rate=48000
    )
    assert disk.exists(target_video_path)