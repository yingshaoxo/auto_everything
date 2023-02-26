#########
# BASIC
#########

#debian
sudo apt -y update
sudo apt -y install gcc
sudo apt -y install g++
sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install python3-dev
sudo apt -y install tmux
sudo apt -y install git

#sudo apt-get -y install python3 python-dev python3-dev \
#     build-essential libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev \
#     python-pip

#arch
sudo pacman --noconfirm -S gcc
sudo pacman --noconfirm -S g++
sudo pacman --noconfirm -S cmake
sudo pacman --noconfirm -S make
sudo pacman --noconfirm -Syu python3
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
rm get-pip.py
#sudo pacman --noconfirm -Syu python-tensorflow-cuda

#macos
case $(uname | tr '[:upper:]' '[:lower:]') in
    linux*)
    ;;
    darwin*)
        export HOMEBREW_INSTALL_FROM_API=1
        export NONINTERACTIVE=1
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        yes | brew install python@3.10
        yes | brew install rustup
        yes | rustup-init
        yes | brew install maturin
    ;;
    msys*)
    ;;
    *)
    ;;
esac

#sudo apt -y install ffmpeg
#sudo apt -y install python3-opencv
#sudo pip3 install git+https://github.com/yingshaoxo/auto_everything.git --upgrade

# #########
# # WITH EXTENSIONS
# #########
# #clear
# echo "Do you wish to install some extensions, so you can use some advanced module later?"
# select yn in "Yes" "No"; do
#     case $yn in
#         Yes ) break;;
#         No ) exit;;
#     esac
# done

# # x11
# sudo apt -y install libx11-dev
# sudo apt -y install libxmu-dev

# # install
# sudo apt -y install git
# if [ ! -d "auto_everything" ]; then
#     # not exist
#     git clone https://github.com/yingshaoxo/auto_everything.git
#     cd auto_everything
# fi
# sudo rm build/* -fr
# sudo rm dist/* -fr
# sudo python3 super_setup.py bdist_wheel
# cd dist
# sudo pip3 install --ignore-installed auto_everything*

# cd ..
# cd auto
# user=$(whoami)
# sudo chown -R $user:$user . 
# python -m pip install --ignore-installed .
# sudo pip3 install --ignore-installed .
# cd ..

# cd example

