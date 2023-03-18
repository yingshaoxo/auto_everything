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

# poetry add --editable .
## poetry add --editable <a_path_towards_the_package_that_is_in_development>
# [tool.poetry.dependencies]
# my-package = {path = "../my/path", develop = true}
