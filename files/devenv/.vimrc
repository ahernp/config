set nocompatible
syntax on
filetype indent plugin on

set path+=**
set wildmenu

set nu
set relativenumber

" Color scheme
set t_Co=256
color wombat256mod
set background=dark

set hlsearch

set tabstop=4
set softtabstop=4
set shiftwidth=4
set shiftround
set expandtab
set autoindent

set laststatus=2

" last-position-jump
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
