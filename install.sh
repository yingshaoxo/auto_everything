user=$(whoami)
sudo chown -R $user:$user . 

pip3 install -e .
sudo pip3 install -e .
