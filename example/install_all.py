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
    "ffmpeg",
    "telegram-desktop",
    "docker",
    "vlc",
    "xournalpp",
    "qv2ray",
    "scrcpy",
    "postman",
    "shotcut",
    "remmina",
    "flameshot",
]

# Use snap on care, it may cut usable permission one by one, in the end, becomes google play store or apple app store, which depresses develop freedom. (And it can't disable auto_update forever.)
for soft in snap_softwares:
    terminal.run(
        f"""
        sudo snap install {soft} --classic
        """
    )
terminal.run(f"""
    sudo snap connect ffmpeg:removable-media
""")


pip_softwares = ["jupyterlab"]

for soft in pip_softwares:
    terminal.run(
        f"""
        sudo pip3 install --no-input {soft}
        """
    )


npm_softwares = ["yarn"]

for soft in npm_softwares:
    terminal.run(
    f"""
    sudo npm install --global --silent {soft}
    """
    )
