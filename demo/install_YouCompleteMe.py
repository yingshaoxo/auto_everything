#!/usr/bin/env python

from auto_everything import base
from os import path

b = base.Terminal()

print("start...\n\n")

# 1
c = """
sudo apt install -y build-essential cmake
sudo apt install -y python3-dev
sudo apt install -y python3-pip
sudo pip3 install -y auto_everything
sudo apt install -y vim
sudo apt install -y git
"""
b.run(c, wait=True)

# 2
if not b.exists("~/.vim/bundle/YouCompleteMe"):
    c = """
cd ~
mkdir .vim
cd .vim
mkdir bundle
cd bundle
git clone --recurse-submodules -j8 https://github.com/Valloric/YouCompleteMe.git
cd YouCompleteMe
python3 ./install.py
    """
    b.run(c, wait=True)

# 3
if not b.exists("~/.vim/bundle/Vundle.vim"):
    c = """
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
    """
    b.run(c, wait=True)

# 4
vimrc = """
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'Valloric/YouCompleteMe'
Plugin 'tell-k/vim-autopep8'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line


au FileType c map <F5> :w<CR>:!gcc % && ./a.out %<CR>
au FileType python map <F5> :w<CR>:!python3.6 %<CR>
au FileType go map <F5> :w<CR>:!go run %<CR>
au FileType sh map <F5> :w<CR>:!bash %<CR>
"<CR> means a Enter key.
"For :w<CR>, I don't know its means.

"autopep8"
autocmd FileType python noremap <buffer> <F8> :call Autopep8()<CR>
let g:autopep8_disable_show_diff=1
"""
with open(b.fix_path("~/.vimrc"), 'w', encoding="utf-8") as f:
    f.write(vimrc)

# 5
c = """
sudo pip3 install autopep8
"""
b.run(c, wait=True)


print("\n\nfinished...")
