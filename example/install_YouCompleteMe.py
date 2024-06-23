#!/usr/bin/env python

from auto_everything.terminal import Terminal
from auto_everything.io import IO
from os import path, geteuid
from sys import platform

t = Terminal()
io_ = IO()

def is_root():
    return geteuid() == 0

if platform == "linux" or platform == "linux2":
    pass
elif platform == "darwin":
    io_.append(
        t.fix_path("~/.zshrc"),
        """
        source ~/.bashrc
        """
    )
elif platform == "win32":
    print("Sorry, we don't support windows")
    exit()

if t.run_command("echo $DESKTOP_SESSION").strip() != "":
    IS_DESKTOP = True
else:
    IS_DESKTOP = False

print("Srript Start...\n\n")

if is_root():
    print("install base dependencies...")
    t.run("""
    sudo apt install -y build-essential cmake
    sudo apt install -y python3-dev
    sudo apt install -y python3-pip
    sudo apt install -y vim
    sudo apt install -y git
    sudo apt install -y curl

    sudo apt install -y golang

    curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    # curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    # source ~/.bashrc
    # nvm install node

    sudo apt-get install -y gcc g++ make

    sudo pacman --noconfirm -S make
    sudo pacman --noconfirm -S cmake
    sudo pacman --noconfirm -S vim
    sudo pacman --noconfirm -S git
    sudo pacman --noconfirm -S curl

    sudo apt install -y tmux
    sudo apt install -y xclip

    git clone https://github.com/preservim/nerdtree.git ~/.vim/pack/vendor/start/nerdtree
    git clone https://github.com/Yggdroot/indentLine.git ~/.vim/pack/vendor/start/indentLine
          """, wait=True)

    if IS_DESKTOP:
        print("install desktop version vim...")
        c = """
        sudo apt-get install vim-gnome -y
        sudo apt-get install vim-gtk3 -y
        sudo pacman --noconfirm -S gvim
        """
        t.run(c, wait=True)

    print("config tmux...")
    io_.write(
        t.fix_path("~/.tmux.conf"),
        """
#set-option -g default-shell "/bin/bash"

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Enable mouse support
setw -g mouse on
#set -g @plugin 'tmux-plugins/tmux-yank'
bind-key -T copy-mode-vi MouseDragEnd1Pane send -X copy-selection-and-cancel\; run "tmux save-buffer - | xclip -i -sel clipboard > /dev/null"

# Enable vim support when ctrl+b+[
# This is for terminal copy and paste
set-window-option -g mode-keys vi
bind-key -T copy-mode-vi v send -X begin-selection
bind-key -T copy-mode-vi V send -X select-line
bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xclip -in -selection clipboard'

# Set new panes to open in current directory
bind c new-window -c "#{pane_current_path}"
bind '"' split-window -c "#{pane_current_path}"
bind % split-window -h -c "#{pane_current_path}"

# Get current working directory for outside program: use $TMUX_WORKING_DIR to get the active dir path of tmux
#set-hook -g pane-focus-in 'if [ -z ${TMUX+x} ]; then eval "export $(tmux show-environment TMUX_WORKING_DIR)"; else tmux setenv TMUX_WORKING_DIR $(pwd); fi'

# Auto save and reload tmux windows
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
set -g @continuum-save-interval '1'

# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
    """.strip(),
    )
    t.run("tmux source ~/.tmux.conf")

    print("config vimrc...")
    vimrc = """
set nocompatible              " be iMproved, required
filetype off                  " required
filetype plugin indent on    " required

au FileType c map <F5> :w<CR>:!gcc % && ./a.out %<CR>
au FileType cpp map <F5> :w<CR>:!gcc % && ./a.out %<CR>
au FileType python map <F5> :w<CR>:!python3 %<CR>
au FileType go map <F5> :w<CR>:!go run %<CR>
au FileType sh map <F5> :w<CR>:!bash %<CR>
au BufRead *.js map <F5> :w<CR>:!node %<CR>

syntax on

set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set fileformat=unix
set number

set clipboard=unnamedplus
vnoremap <silent><Leader>y "yy <Bar> :call system('xclip -sel clipboard', @y)<CR>
"select, then use \y to copy it into clipboard

"hide thing on gvim
set guioptions-=m  "menu bar
set guioptions-=T  "toolbar
set guioptions-=r  "scrollbar
let g:autopep8_max_line_length=10000
set backupcopy=yes

"for NERDTree"
nnoremap <C-\> :NERDTreeToggle<CR>
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * NERDTree | if argc() > 0 || exists("s:std_in") | wincmd p | endif

"no auto indent
filetype indent off
set noai

"show json quotes
let g:vim_json_conceal=0

"disable dark mode
set background=light
    """
    with open(t.fix_path("~/.vimrc"), "w", encoding="utf-8") as f:
        f.write(vimrc)

    print("install auto_everything...")
    t.run("""
    sudo pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev"
    sudo pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev" --break-system-packages
    """, wait=True)

    print("config bashrc")
    io_.append(
        t.fix_path("~/.bashrc"),
        """
    #if [ -z ${TMUX+x} ]; then eval "export $(tmux show-environment TMUX_WORKING_DIR)" && cd $TMUX_WORKING_DIR; else tmux setenv TMUX_WORKING_DIR $(pwd); fi

    export PATH="$PATH:/home/yingshaoxo/.auto_everything/bin"

    export PROMPT_COMMAND="history -a; history -n"
        """
    )

    print("done")
    last = """
\n\n\n
There just left two thing for you to do:
    1. start tmux by `tmux`
        then type
            `ctrl+b+I`
    2. run `sudo vim`, and hit `ctrl+\` to trigger file exploer
    3. you can use `ctrl+p` to auto_complete in vim
Enjoy!
    """
    print(last)
else:
    # 1
    print("install building tools...")
    c = """
    sudo -S apt update

    sudo apt install -y build-essential cmake
    sudo apt install -y python3-dev
    sudo apt install -y python3-pip
    sudo apt install -y vim
    sudo apt install -y git
    sudo apt install -y curl

    sudo apt install -y golang

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    source ~/.bashrc
    nvm install node

    sudo apt-get install -y gcc g++ make

    sudo pacman --noconfirm -S make
    sudo pacman --noconfirm -S cmake
    sudo pacman --noconfirm -S vim
    sudo pacman --noconfirm -S git
    sudo pacman --noconfirm -S curl

    sudo apt install -y terminator
    sudo apt install -y tmux
    sudo apt install -y xclip
    """
    t.run(c, wait=True)

    # 2
    if not t.exists("~/.vim/bundle/YouCompleteMe"):
        print("install YouCompleteMe...")
        c = """
    mkdir -p ~/.vim/bundle
    cd ~/.vim/bundle
    git clone --recurse-submodules -j8 https://github.com/ycm-core/YouCompleteMe.git
    cd YouCompleteMe
    python3 install.py --all
        """
        t.run(c, wait=True)

    # 3
    if not t.exists("~/.vim/bundle/Vundle.vim"):
        print("install Vundle...")
        c = """
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
    git clone https://github.com/leafgarland/typescript-vim.git ~/.vim/bundle/typescript-vim
        """
        t.run(c, wait=True)

    # 4
    print("setup .vimrc...")
    vimrc = """
    set nocompatible              " be iMproved, required
    filetype off                  " required

    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
    Plugin 'VundleVim/Vundle.vim'
    Plugin 'Valloric/YouCompleteMe'
    Plugin 'tell-k/vim-autopep8'
    Plugin 'leafgarland/typescript-vim'
    Plugin 'Chiel92/vim-autoformat'
    Plugin 'fatih/vim-go'
    Plugin 'pangloss/vim-javascript'
    Plugin 'mxw/vim-jsx'
    Plugin 'preservim/nerdtree'
    call vundle#end()            " required

    filetype plugin indent on    " required

    au FileType c map <F5> :w<CR>:!gcc % && ./a.out %<CR>
    au FileType cpp map <F5> :w<CR>:!gcc % && ./a.out %<CR>
    au FileType python map <F5> :w<CR>:!python3 %<CR>
    au FileType go map <F5> :w<CR>:!go run %<CR>
    au FileType sh map <F5> :w<CR>:!bash %<CR>
    au BufRead *.js map <F5> :w<CR>:!node %<CR>

    autocmd FileType python noremap <buffer> <F8> :call Autopep8()<CR>
    autocmd FileType go noremap <buffer> <F8> :GoFmt<CR>
    autocmd FileType javascript noremap <buffer> <F8> :Autoformat<CR>
    let g:autopep8_disable_show_diff=1
    syntax on

    set tabstop=4
    set softtabstop=4
    set shiftwidth=4
    set expandtab
    set fileformat=unix
    set number

    set clipboard=unnamedplus

    "hide thing on gvim
    set guioptions-=m  "menu bar
    set guioptions-=T  "toolbar
    set guioptions-=r  "scrollbar
    let g:autopep8_max_line_length=10000
    set backupcopy=yes

    "for NERDTree"
    nnoremap <C-\> :NERDTreeToggle<CR>
    autocmd StdinReadPre * let s:std_in=1
    autocmd VimEnter * NERDTree | if argc() > 0 || exists("s:std_in") | wincmd p | endif

    set completeopt-=preview

    "no auto indent
    filetype indent off

    let g:vim_json_conceal=0

    set background=light

    let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'
    """
    with open(t.fix_path("~/.vimrc"), "w", encoding="utf-8") as f:
        f.write(vimrc)

    if platform == "darwin":
        more_config_for_macos_vim = "\n\nset clipboard=unnamed"
        with open(t.fix_path("~/.vimrc"), "a", encoding="utf-8") as f:
            f.write(vimrc)

    # 5
    print("setup desktop vim...")
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

    # 5.5, for autopep
    print("setup f8 autopep...")
    path = t.fix_path("~/.vim")
    if not t.exists(f"{path}/plugin"):
        t.run(
            f"""
        cd {path}
        sudo mkdir -p {path}/plugin
        """
        )
    t.run(
        f"""
    cd {path}/plugin
    sudo wget https://github.com/tell-k/vim-autopep8/raw/master/ftplugin/python_autopep8.vim
    """
    )

    # 5.8, for python indent line
    t.run(
        f"""
    git clone https://github.com/Yggdroot/indentLine.git ~/.vim/pack/vendor/start/indentLine
    """
    )

    # 5.9, for pure c completion
    ycm_extra_configuration = """
def Settings( **kwargs ):
    return {
        'flags': [
            '-std=gnu99',
            #'-std=c99',
            '-x', 'c',

            #'-std=cpp11',
            #'-x', 'c++',

            '-static',
            '-no-pie',
            #'-D_POSIX_SOURCE',
        ],
    }
    """.strip()
    ycm_configuration_path = "~/.vim/.ycm_extra_conf.py"
    ycm_configuration_path = terminal.fix_path(ycm_configuration_path)
    io_.write(ycm_configuration_path, ycm_extra_configuration)

    # 6 set terminator
    print("setup terminator configs...")
    t.run(
        """
    mkdir -p ~/.config/terminator/
    """
    )
    io_.write(
        t.fix_path("~/.config/terminator/config"),
        """
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
    """,
    )


    # 8 config tmux
    print("config tmux...")

    io_.write(
        t.fix_path("~/.tmux.conf"),
        """
    #set-option -g default-shell "/bin/bash"

    set -g @plugin 'tmux-plugins/tpm'
    set -g @plugin 'tmux-plugins/tmux-sensible'

    # Enable mouse support
    setw -g mouse on
    #set -g @plugin 'tmux-plugins/tmux-yank'
    bind-key -T copy-mode-vi MouseDragEnd1Pane send -X copy-selection-and-cancel\; run "tmux save-buffer - | xclip -i -sel clipboard > /dev/null"

    # Enable vim support when ctrl+b+[
    # This is for terminal copy and paste
    set-window-option -g mode-keys vi
    bind-key -T copy-mode-vi v send -X begin-selection
    bind-key -T copy-mode-vi V send -X select-line
    bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xclip -in -selection clipboard'

    # Set new panes to open in current directory
    bind c new-window -c "#{pane_current_path}"
    bind '"' split-window -c "#{pane_current_path}"
    bind % split-window -h -c "#{pane_current_path}"

    # Get current working directory for outside program: use $TMUX_WORKING_DIR to get the active dir path of tmux
    #set-hook -g pane-focus-in 'if [ -z ${TMUX+x} ]; then eval "export $(tmux show-environment TMUX_WORKING_DIR)"; else tmux setenv TMUX_WORKING_DIR $(pwd); fi'

    # Auto save and reload tmux windows
    set -g @plugin 'tmux-plugins/tmux-resurrect'
    set -g @plugin 'tmux-plugins/tmux-continuum'
    set -g @continuum-restore 'on'
    set -g @continuum-save-interval '1'

    # Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
    run '~/.tmux/plugins/tpm/tpm'
    """,
    )
    t.run("tmux source ~/.tmux.conf")


    print("install auto_everything...")
    t.run("""
    pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev"
    pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev" --break-system-packages
    """, wait=True)

    # 8 config bashrc
    print("config bashrc")
    io_.append(
        t.fix_path("~/.bashrc"),
        """
    #if [ -z ${TMUX+x} ]; then eval "export $(tmux show-environment TMUX_WORKING_DIR)" && cd $TMUX_WORKING_DIR; else tmux setenv TMUX_WORKING_DIR $(pwd); fi
    #clear

    export PATH="$PATH:/home/yingshaoxo/go/bin"
    export PATH="$PATH:/home/yingshaoxo/.auto_everything/bin"

    export PROMPT_COMMAND="history -a; history -n"
        """
    )

    print("done")
    last = """
    \n\n\n
    There just left two thing for you to do:
        1. start tmux by `tmux`
            then type
                `ctrl+b+I`
        2. start vim by `vim`
            then type
                `:PluginInstall`
            > ctrl+w+w to switch between sub_window in vim
    After these, enjoy!
    """
    print(last)
