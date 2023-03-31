#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()


class Tools():
    def push(self, comment: str):
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
        # sudo pip3 install pytest
        # sudo pip3 install -e .
        t.run("""
        pytest
""")

    def check(self, py_file: str|None=None):
        if py_file is None:
            t.run("""
            prospector
            """)
        else:
            t.run(f"""
            prospector {py_file}
            """)

    def install(self, method:int=0):
        print(method)
        if method == 0:
            t.run("""
    sudo pip3 install -e .
    pip3 install -e .
            """)
        else:
            t.run("""
    sudo rm -fr dist
    sudo rm -fr build

    sudo pip3 uninstall -y auto_everything
    sudo -H python3 setup.py sdist bdist_wheel
    cd dist
    sudo pip3 install auto_everything*

    #sudo pip3 install -e .[video]
    #sudo pip3 install .
    cd ..
            """)

    def make_docs(self):
        t.run("""
        sudo apt install -y python3-sphinx
        #brew install sphinx-doc
        pip3 install Flask-Sphinx-Themes
        cd docs
        make html
        cp -fr docs/html/* .
        rm -fr docs
        """)

    def publish(self):
        self.install()
        self.make_docs()
        t.run("""
        sudo apt install -y twine
        """)
        print("Input your username of pypi:")
        t.run("""
twine upload dist/*
        """)


py.make_it_runnable()
py.fire(Tools)
