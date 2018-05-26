#!/usr/bin/env python

from auto_everything import base
from os import path

b = base.Terminal()

print("start...\n\n")

c = """
sudo wget https://dl.google.com/go/go1.10.2.linux-amd64.tar.gz
sudo tar -xvf go*linux-amd64.tar.gz
sudo rm /usr/local/go -fr
sudo mv go /usr/local
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
source ~/.profile
sudo rm go*linux-amd64.tar.gz
"""

b.run(c, wait=True)
