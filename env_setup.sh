sudo apt -y install python3
sudo apt -y install python3-pip

sudo pacman --noconfirm -Syu python-tensorflow-cuda
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pacman --noconfirm -S cmake
sudo pacman --noconfirm -S make

#sudo apt install ffmpeg

sudo pip3 install auto_everything --upgrade
