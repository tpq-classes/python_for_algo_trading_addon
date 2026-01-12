"
" This is an example file for:
" ~/.vimrc
"
" It configures some useful features
" for Python development and other purposes.
"
" It is to be saved in user home with name ".vimrc"
" i.e. at location "~/.vimrc"
"
" change "~/.inputrc" to include
" set editing-mode vi
"

" auto-completion for Python files
set completeopt=menu,noinsert
set complete=k**/*.py

" show line numbers
set number

" set tabs to have 4 spaces
set ts=4

" indent when moving to the next line while writing code
set autoindent

" expand tabs into spaces
set expandtab

" when using the >> or << commands, shift lines by 4 spaces
set shiftwidth=4

" show a visual line under the cursor's current line
set cursorline

" show the matching part of the pair for [] {} and ()
set showmatch

" enable all Python syntax highlighting features
let python_highlight_all = 1

" set register to clipboard
set clipboard=unnamed

" cursor placement via mouse click
set mouse=a

" Python formatting specifics
set tabstop=8
set softtabstop=4
filetype indent on

" Set ruler and line wrap
set colorcolumn=80
set textwidth=85

" executing current Python script via
" CTRL+x (python) or via CTRL+SHIFT+x (python3)
map <C-x> :w<CR>:!python %<CR>
map <C-S-x> :w<CR>:!python3 %<CR>

" remote terminal arrow keys fix
set term=ansi

" enable syntax highlighting
syntax enable
