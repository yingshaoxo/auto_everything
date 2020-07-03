#debian
sudo apt -y update
sudo apt -y install gcc
sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install python3-dev

#sudo apt-get -y install python3 python-dev python3-dev \
#     build-essential libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev \
#     python-pip

#arch
sudo pacman --noconfirm -S gcc
sudo pacman --noconfirm -S cmake
sudo pacman --noconfirm -S make
sudo pacman --noconfirm -Syu python3
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
#sudo pacman --noconfirm -Syu python-tensorflow-cuda

#sudo apt -y install ffmpeg
#sudo apt -y install python3-opencv
sudo pip3 install auto_everything --upgrade
