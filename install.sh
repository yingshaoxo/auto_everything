#/bin/bash
source ~/.bashrc

#user=$(whoami)
#sudo chown -R $user:$user . 
#
#pip3 install -e .
#sudo pip3 install -e .

deactivate
rm -fr dist/*
poetry build
python -m pip install dist/*.whl  --force-reinstall 
