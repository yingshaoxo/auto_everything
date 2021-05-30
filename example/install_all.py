from auto_everything.all import *


terminal.debug = True


apt_softwares = [
    "code",
    "xclip",
    "snapd",
]

for soft in apt_softwares:
    terminal.run(
        f"""
        sudo apt install -y {soft}                                                                                      
        """
    )


snap_softwares = [
    "obs-studio",
    "qv2ray",
    "postman",
    "shotcut",
    "ffmpeg",
    "docker",
    "xournalpp",
    "telegram-desktop",
    "remmina",
    "flameshot",
]

for soft in snap_softwares:
    terminal.run(
        f"""
        sudo snap install {soft} --classic
        """
    )


pip_softwares = ["jupyterlab"]

for soft in pip_softwares:
    terminal.run(
        f"""
        sudo pip3 install --no-input {soft}
        """
    )
