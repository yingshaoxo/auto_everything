from auto_everything.disk import Disk
disk = Disk()


class GlobalStore:
    def __init__(self) -> None:
        self.DATABASE_URL = "sqlite:///auto_everything_service.db"
        self.tempFolder = disk.concatenate_paths(
            disk.get_the_temp_dir(), "auto_everything_service")
        disk.create_a_folder(self.tempFolder)
