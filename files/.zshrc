# Load and run compinit
autoload -U compinit zcalc zmv
compinit -i

# Prompts
# Autoload zsh add-zsh-hook and vcs_info functions (-U autoload w/o substition, -z use zsh style)
autoload -Uz add-zsh-hook vcs_info
# Enable substitution in the prompt.
setopt prompt_subst
# Run vcs_info just before a prompt is displayed (precmd)
add-zsh-hook precmd vcs_info
# add ${vcs_info_msg_0} to the prompt
# e.g. here we add the Git information in cyan
PROMPT='%~ %F{cyan}${vcs_info_msg_0_}%f'

# Enable checking for (un)staged changes, enabling use of %u and %c
zstyle ':vcs_info:*' check-for-changes true
# Set custom strings for an unstaged vcs repo changes (*) and staged changes (+)
zstyle ':vcs_info:*' unstagedstr ' *'
zstyle ':vcs_info:*' stagedstr ' +'
# Set the format of the Git information for vcs_info
zstyle ':vcs_info:git:*' formats       '(%b%u%c) '
zstyle ':vcs_info:git:*' actionformats '(%b|%a%u%c) '

RPROMPT="(%n@%m)"

alias ls="eza -F"
alias ll="eza -alhF"
alias tree="eza --tree --long -a --git-ignore"
alias cat="batcat"
alias backup="cd ~;fab backup;cd -"
alias tz="fab times"
alias up="sudo apt update && sudo apt upgrade -y"
alias cal="ncal -byM"
alias fzf='fzf --preview "batcat --color=always --style=numbers --line-range=:500 {}"'
alias dev="cd ~/code/ahernp.com;source venv/bin/activate"
alias run="cd ~/code/ahernp.com;source venv/bin/activate;python manage.py runserver --settings project.dev_settings"

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
bindkey '^[OA' history-beginning-search-backward
bindkey '^[OB' history-beginning-search-forward

neofetch
uptime
