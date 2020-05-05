
        sudo apt install python3-sphinx
        sudo pip3 install Flask-Sphinx-Themes
        cd docs
        make html
        cp docs/html/* . -fr
        rm docs -fr
        