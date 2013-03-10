# Load and run compinit
autoload -U compinit
compinit -i

# Prompts
setopt prompt_subst
autoload -U colors && colors
RPROMPT='${PWD/#$HOME/~} (%n@%m)'
# vcprompt must be installed for this to work (http://vc.gerg.ca/hg/vcprompt/)
PROMPT='%{$fg_bold[green]%}%p%{$fg[cyan]%}%c %{$fg_bold[blue]%}$(vcprompt)%{$reset_color%}'

export EDITOR="vi"
alias ls='ls -Fh --color=auto'
alias glog='hg glog -l9 --style compact'
alias test='fab manage:test'
alias run='fab manage:runserver'
alias backup='cd ~;fab backup;cd -'
alias ack='ack-grep'
alias vi='vi -p'

# Virtual environments
export WORKON_HOME=~/code
source /usr/local/bin/virtualenvwrapper.sh

# Show function names
echo "User-defined zsh functions"
grep "() {" ~/.zshrc
dmcm() {workon dmcm;cd ~/code/dmcm/project}

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

# Keybindings
bindkey "^[[1~"  beginning-of-line
bindkey "^[[4~"  end-of-line
bindkey "^[[3~"  delete-char
bindkey "^[3;5~" delete-char
