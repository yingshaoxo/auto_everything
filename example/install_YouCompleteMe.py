
#!/usr/bin/env python                                                                           
                                                                                                
from auto_everything.base import Terminal, IO                                                   
from os import path                                                                             
                                                                                                
t = Terminal()                                                                                  
io = IO()                                                                                       
                                                                                                              
if (t.run_command("echo $DESKTOP_SESSION").strip() != ""):
    IS_DESKTOP = True
else:
    IS_DESKTOP = False

print("start...\n\n")                                                                                         
                                                                                                              
# 1                                                                                                           
c = """                                                                                                       
sudo apt install -y build-essential cmake                                                                                        
sudo apt install -y python3-dev                                                                                                  
sudo apt install -y python3-pip                                                                                                  
sudo apt install -y vim                                                                                                                                    
sudo apt install -y git                                                                                                                                    
sudo apt install -y curl                                                                                                                                   

sudo apt install -y golang
curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y gcc g++ make 
sudo apt-get install -y nodejs

sudo pacman --noconfirm -S make
sudo pacman --noconfirm -S cmake
sudo pacman --noconfirm -S vim
sudo pacman --noconfirm -S git
sudo pacman --noconfirm -S curl
"""
t.run(c, wait=True)

# 2
if not t.exists("~/.vim/bundle/YouCompleteMe"):
    c = """
cd ~
mkdir .vim
cd .vim
mkdir bundle
cd bundle
git clone --recurse-submodules -j8 https://github.com/ycm-core/YouCompleteMe.git
cd YouCompleteMe
sudo python3 ./install.py
    """
    t.run(c, wait=True)

# 3
if not t.exists("~/.vim/bundle/Vundle.vim"):
    c = """
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
git clone https://github.com/leafgarland/typescript-vim.git ~/.vim/bundle/typescript-vim
    """
    t.run(c, wait=True)

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
Plugin 'leafgarland/typescript-vim'
Plugin 'Chiel92/vim-autoformat'
Plugin 'fatih/vim-go'
Plugin 'pangloss/vim-javascript'
Plugin 'mxw/vim-jsx'
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
au FileType cpp map <F5> :w<CR>:!gcc % && ./a.out %<CR>
au FileType python map <F5> :w<CR>:!python3 %<CR>
au FileType go map <F5> :w<CR>:!go run %<CR>
au FileType sh map <F5> :w<CR>:!bash %<CR>
au BufRead *.js map <F5> :w<CR>:!node %<CR>
"<CR> means a Enter key.
"For :w<CR>, I don't know its means.
"autopep8"
autocmd FileType python noremap <buffer> <F8> :call Autopep8()<CR>
autocmd FileType go noremap <buffer> <F8> :GoFmt<CR>
autocmd FileType javascript noremap <buffer> <F8> :Autoformat<CR>
let g:autopep8_disable_show_diff=1
syntax on
"input behavior"
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set fileformat=unix
" set autoindent
" autoindent may cause bad behavior when you paste in vim
set clipboard=unnamedplus
"hide thing on gvim
set guioptions-=m  "menu bar
set guioptions-=T  "toolbar
set guioptions-=r  "scrollbar
let g:autopep8_max_line_length=10000
set backupcopy=yes
"""
with open(t.fix_path("~/.vimrc"), 'w', encoding="utf-8") as f:
    f.write(vimrc)

# 5
c = """
sudo pip3 install autopep8
sudo pip3 install jedi
"""
t.run(c, wait=True)

if IS_DESKTOP:
    c = """
    sudo apt-get install vim-gnome -y
    sudo apt-get install vim-gtk3 -y
    sudo pacman --noconfirm -S gvim
    """
    t.run(c, wait=True)


print("\n\nfinished...")


# 5.5, for autopep
path = t.fix_path("~/.vim")
if not t.exists(f"{path}/plugin"):
    t.run(f"""
    cd {path}
    sudo mkdir -p {path}/plugin
    """)
t.run(f"""
cd {path}/plugin
sudo wget https://github.com/tell-k/vim-autopep8/raw/master/ftplugin/python_autopep8.vim
""")


# 6 set terminator
t.run("""
mkdir -p ~/.config/terminator/
touch config
""")
io.write(t.fix_path('~/.config/terminator/config'), """
[global_config]
  always_split_with_profile = True
  borderless = True
  smart_copy = False
  suppress_multiple_term_dialog = True
  window_state = maximise
[keybindings]
  broadcast_all = None
  broadcast_group = None
  broadcast_off = None
[layouts]
  [[default]]
    [[[child1]]]
      parent = window0
      type = Terminal
    [[[window0]]]
      parent = ""
      type = Window
[plugins]
[profiles]
  [[default]]
    cursor_color = "#aaaaaa"
    icon_bell = False
    scrollbar_position = hidden
    scrollback_infinite = True
    show_titlebar = False
  [[mine]]
    cursor_color = "#aaaaaa"
    font = Monospace 30
    icon_bell = False
    scrollbar_position = hidden
    show_titlebar = False
    use_system_font = False
""")


# 7 copy file to root
c = """
sudo cp ~/.vim /root/.vim -r
sudo cp ~/.vimrc /root/.vimrc
"""
t.run(c, wait=True)


last = """
\n\n\n
There just left one thing you have to do:
    start vim by `sudo vim`
        then type
            `:PluginInstall`
After this, enjoy!
"""
print(last)