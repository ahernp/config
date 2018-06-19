# Load and run compinit
autoload -U compinit zcalc zmv
compinit -i

# Prompts
setopt prompt_subst
autoload -U colors && colors
RPROMPT='${PWD/#$HOME/~} (%n@%m)'
# vcprompt must be installed for this to work (see https://github.com/djl/vcprompt)
PROMPT='%{$fg_bold[green]%}%p%{$fg[cyan]%}%c%{$fg_bold[blue]%} $(vcprompt)%{$reset_color%} '

export EDITOR="vi"
alias ls='ls -Fh --color=auto'
alias test='fab test'
alias backup='cd ~;fab backup;cd -'
alias vi='vi -p'
alias port='docker run --name portainer --restart=always -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer'
alias de='cd ~/code;docker-compose'
alias doc='de up'
alias sql='de exec db psql -U postgres ahernp'
alias app='de exec webapp bash'
alias dev='de exec devenv bash'

grep "alias " ~/.zshrc

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

# Activate zshrc syntax highlighting
source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
