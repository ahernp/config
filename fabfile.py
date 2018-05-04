"""
Setup Ubuntu PC.
"""
from fabric.contrib.files import exists, is_link

import os
from datetime import datetime
from fabric.api import task, hosts, local, env, settings
from fabric.colors import magenta
from fabric.context_managers import lcd

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.environ.get('HOME')

@task
@hosts('localhost')
def setup_pc():
    """Setup Ubuntu Desktop PC."""

    APT_PACKAGES = ['byobu', 'calibre', 'geany', 'geany-plugins', 'git', 'gnucash', 'htop',
                    'screen', 'silversearcher-ag', 'speedcrunch', 'tree', 'vim', 'vlc', 'zsh']
    with settings(prompts={'Do you want to continue [Y/n]? ': 'Y'}):
        local('sudo apt install {packages}'.format(packages=' '.join(APT_PACKAGES)))

    # Create link for .ssh
    link_path = '~/.ssh'
    if is_link(link_path):
        local('rm {link_path}'.format(link_path=link_path))
    work_dot_ssh_path = '~/Desktop/work/dot.ssh'
    if exists(work_dot_ssh_path):
        local('ln -s {dir_path} {link_path}'.format(dir_path=work_dot_ssh_path, link_path=link_path))
    local('chmod o-rx ~/.ssh/github/id_rsa')
    local('chmod g-rx ~/.ssh/github/id_rsa')
    local('chmod o-rx ~/.ssh/id_rsa')
    local('chmod g-rx ~/.ssh/id_rsa')

    # Add links to config files to home directory
    for filename in ['.gitconfig', '.vimrc', '.zsh_history', '.zshrc', 'fabfile.py']:
        link_path = '~/{link}'.format(link=filename)
        if is_link(link_path):
            local('rm {link_path}'.format(link_path=link_path))
        file_path = '{curr_dir}/files/{filename}'.format(curr_dir=CURR_DIR, filename=filename)
        local('ln -s {file_path} {link_path}'.format(file_path=file_path, link_path=link_path))

    # vim
    local('git clone https://github.com/VundleVim/Vundle.vim ~/.vim/bundle/vundle.vim '
          '|| cd ~/.vim/bundle/vundle.vim; git pull')
    local('git clone https://github.com/leafgarland/typescript-vim.git ~/.vim/bundle/typescript-vim.vim '
          '|| cd ~/.vim/bundle/typescript-vim.vim; git pull')
    link_path = '~/.vim/colors'
    if is_link(link_path):
        local('rm {link_path}'.format(link_path=link_path))
    file_path = '{curr_dir}/files/.vim/colors'.format(curr_dir=CURR_DIR)
    local('ln -s {file_path} ~/.vim/colors'.format(file_path=file_path)
    local('vim +BundleInstall +qall')

    # Byobu
    if not exists('~/.byobu/backend'):
        local('byobu-select-backend screen')
	local('cp {curr_dir}/files/byobu.desktop .local/share/applications/byobu.desktop'.format(curr_dir=curr_dir)

    # vcprompt
    if not exists('/usr/local/bin/vcprompt'):
        local('sudo ln -s {curr_dir}/files/vcprompt /usr/local/bin/vcprompt'.format(curr_dir=CURR_DIR))
    #local('chmod a+x {curr_dir}/files/vcprompt'.format(curr_dir=CURR_DIR))

    local('sudo cp {curr_dir}/files/hosts /etc/hosts')
    local('sudo chmod u=rw,g=r,o=r /etc/hosts')

    # Switch to .zshrc
    local('chsh -s /usr/bin/zsh')
    local('sudo git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /usr/local/share/zsh-syntax-highlighting '
          '|| cd /usr/local/share/zsh-syntax-highlighting; sudo git pull')

	# Docker
	with lcd('/tmp'):
		local('curl -fsSL get.docker.com -o get-docker.sh')
		local('sudo sh get-docker.sh')

	# Atom
	local('curl -L https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -')
	local('sudo sh -c \'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list\'')
	local('sudo apt-get update')
	local('sudo apt-get install atom')
