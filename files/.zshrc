# Load and run compinit
autoload -U compinit zcalc zmv
compinit -i

# Prompts
setopt prompt_subst
autoload -U colors && colors
RPROMPT="${PWD/#$HOME/~} (%n@%m)"
# vcprompt must be installed for this to work (see https://github.com/djl/vcprompt)
PROMPT='%{$fg_bold[green]%}%p%{$fg[cyan]%}%c%{$fg_bold[blue]%} $(vcprompt -f '%m%a%u')%{$reset_color%} '

alias ls="exa -F"
alias ll="exa -Falh"
alias tree="exa --tree"
alias cat="batcat"
alias backup="cd ~;fab backup;cd -"
alias tz="fab times"
alias up="sudo apt update && sudo apt upgrade -y"
alias cal="ncal -byM"
alias pmcm="cd ~/code/pmcm;./startup.sh"
alias fzf='fzf --preview "batcat --color=always --style=numbers --line-range=:500 {}"'

grep "^alias " ~/.zshrc

# zsh history
HISTFILE=~/.zsh_history
SAVEHIST=10000
HISTSIZE=10000
setopt APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE
setopt HIST_NO_STORE
setopt HIST_SAVE_NO_DUPS
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_FIND_NO_DUPS

# Stop using C-s for XOFF
stty -ixon

# Activate zshrc syntax highlighting
source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Set up fzf key bindings and fuzzy completion
# Needs version 0.48 or later
source <(fzf --zsh)

# Enable history arrow search
bindkey '^[OA' history-search-backward
bindkey '^[OB' history-search-forward

fab numbers-of-days
