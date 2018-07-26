sudo apt -y install python3
sudo apt -y install python3-pip

sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo cp /usr/bin/python3.6 /usr/bin/python3
sudo yum -y install python36u-pip
sudo cp /usr/bin/pip3.6 /usr/bin/pip3
sudo yum -y install python36u-devel

sudo pip3 install auto_everything --upgrade
