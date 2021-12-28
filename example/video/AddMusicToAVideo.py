from auto_everything.video import Video

video = Video()

video.addMusicFilesToVideoFile(
    source_file_path="input.mp4",
    target_file_path="output.mp4",
    musicFiles=[
        "/Users/yingshaoxo/Downloads/永远都会在 - 旅行团乐队.mp3",
        "/Users/yingshaoxo/Downloads/wish you were gay - Billie Eilish.mp3"
    ],
    preDecreaseDBValueForTheMusic=18,
    howManyDBYouWannaTheMusicToDecreaseWhenYouSpeak=15,
)