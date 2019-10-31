#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()


class Tools():
    def push(self, comment):
        self.__clear()
        self.make_docs()

        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def test(self):
        t.run("""
        pytest
        """)

    def check(self, py_file=None):
        if py_file is None:
            t.run("""
            prospector
            """)
        else:
            t.run(f"""
            prospector {py_file}
            """)

    def install(self):
        t.run("""
sudo rm -fr dist
sudo rm -fr build

sudo pip3 uninstall -y auto_everything
sudo -H python3 setup.py sdist bdist_wheel
cd dist
sudo pip3 install auto_everything*
cd ..
        """)

    def make_docs(self):
        t.run("""
        sudo apt install python3-sphinx
        sudo pip3 install Flask-Sphinx-Themes
        cd docs
        make html
        cp docs/html/* . -fr
        rm docs -fr
        """)

    def publish(self):
        self.install()
        self.make_docs()
        t.run("""
twine upload dist/*
        """)

    def __clear(self):
        commands = """
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
        """
        t.run(commands)


py.make_it_runnable()
py.fire(Tools)
