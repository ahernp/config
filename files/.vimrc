if &diff
    syntax off
    colorscheme evening
else
    syntax on
    colorscheme habamax
endif
au VimEnter * if &diff | execute 'windo set wrap' | endif
