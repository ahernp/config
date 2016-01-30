" Use Vundle to manage plugins
" git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim/
call vundle#rc()

Bundle 'Lokaltog/vim-powerline'
Bundle 'kien/ctrlp.vim'
Plugin 'SirVer/ultisnips'
Plugin 'honza/vim-snippets'
"Plugin 'altercation/vim-colors-solarized'

filetype plugin indent on

" Settings for vim-powerline
set laststatus=2

" Settings for ctrlp
let g:ctrlp_max_height=30
let g:ctrlp_follow_symlinks=1
set wildignore+=*.pyc
set wildignore+=*_build/*
set wildignore+=*/coverage/*

" Settings for ultisnips
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-j>"
let g:UltiSnipsJumpBackwardTrigger="<c-k>"
let g:UltiSnipsEditSplit="horizontal"


" Automatic reloading of .vimrc
autocmd! bufwritepost .vimrc source %

" Backspace
set bs=2     " make backspace behave like normal again

" Rebind <Leader> key
let mapleader = ","

" map sort function to a key
vnoremap <Leader>s :sort<CR>

" Show whitespace
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
au InsertLeave * match ExtraWhitespace /\s\+$/

" Color scheme
" mkdir -p ~/.vim/colors && cd ~/.vim/colors
" wget -O wombat256mod.vim https://raw.githubusercontent.com/ahernp/config/master/wombat256mod.vim
set t_Co=256
color wombat256mod
syntax enable
set background=dark
"colorscheme solarized

" Enable syntax highlighting
filetype off
filetype plugin indent on
syntax on

" Showing line numbers and length
set number  " show line numbers
set tw=79   " width of document (used by gd)
set nowrap  " don't automatically wrap on load
set fo-=t   " don't automatically wrap text when typing
set colorcolumn=80
highlight ColorColumn ctermbg=233

" Useful settings
set history=700
set undolevels=700
set tabstop=4
set softtabstop=4
set shiftwidth=4
set shiftround
set expandtab

" Make search case insensitive
set hlsearch
set incsearch
set ignorecase
set smartcase

" Insert a python breakpoint
map <Leader>b Oimport pdb; pdb.set_trace() # BREAKPOINT<C-c>

" When editing a file, always jump to the last known cursor position.
if has("autocmd")
    au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
endif

" Use arrow to navigate between tabs and buffers
nmap <up>       :bp<CR>
nmap <down>     :bn<CR>
nmap <left>     :tabp<CR>
nmap <right>    :tabn<CR>

" Use backspace to clear highlighting
nmap <backspace> :noh<CR>

" Highlight cursor
"set cursorline
"set cursorcolumn

" Paste from clipboard.
map <Leader>p :set paste<CR>o<ESC>]p:set nopaste<cr>

" Treat everything as UTF-8
set encoding=utf-8
set fileencodings=utf-8
