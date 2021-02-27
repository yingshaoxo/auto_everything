from auto_everything.io import IO
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk
from auto_everything.python import Python
from auto_everything.network import Network

__all__ = [
    IO,
    Terminal,
    Disk,
    Python,
    Network
]

"""
try:
    from auto_everything.video import Video, DeepVideo
    from auto_everything.web import Selenium
    __all__ += [
        Video,
        DeepVideo,
        Selenium
    ]
except Exception:
    pass
"""
