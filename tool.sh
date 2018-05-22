#!/bin/bash

clear() {
	sudo rm -fr dist
	sudo rm -fr build
	sudo rm -fr test.py
	sudo rm -fr nohup.out
	sudo rm -fr whatsup.log
	sudo rm -fr auto_everything.egg-info
	sudo rm auto_everything/Base.pyc
	sudo rm auto_everything/__init__.pyc
	sudo rm -fr auto_everything/nohup.out
	sudo rm -fr auto_everything/__pycache__
}

test() {
	clear
	sudo pip3 uninstall -y auto_everything
	python3 setup.py sdist bdist_wheel
	cd dist
	sudo pip3 install auto_everything*
	cd ..
}

publish() {
	twine upload dist/*
}

pull() {
	git fetch --all
	git reset --hard origin/master
}

push() {
	clear
	git config --global user.email "yingshaoxo@gmail.com"
	git config --global user.name "yingshaoxo"
	git add .
	git commit -m "update"
	git push origin
}


if [ "$1" == "clear" ]; then
    clear

elif [ "$1" == "test" ]; then
    test

elif [ "$1" == "publish" ]; then
    publish

elif [ "$1" == "pull" ]; then
    pull

elif [ "$1" == "push" ]; then
    push

elif [ "$1" == "" ]; then
    echo "clear
test
publish
pull
push"

fi
