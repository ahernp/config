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

    APT_PACKAGES = ['brasero', 'byobu', 'calibre', 'geany', 'geany-plugins', 'git', 'gnucash', 'htop',
                    'silversearcher-ag', 'speedcrunch', 'tree', 'vim', 'zsh']
    with settings(prompts={'Do you want to continue [Y/n]? ': 'Y'}):
        local('sudo apt install {packages}'.format(packages=' '.join(APT_PACKAGES)))

    # Create link for .ssh
    link_path = '~/.ssh'
    if is_link(link_path):
        local('rm {link_path}'.format(link_path=link_path))
    work_dot_ssh_path = '~/Desktop/work/dot.ssh'
    if exists(work_dot_ssh_path):
        local('ln -s {dir_path} {link_path}'.format(dir_path=work_dot_ssh_path, link_path=link_path))

    # Add links to config files to home directory
    for filename in ['.gitconfig', '.vimrc', '.zsh_history', '.zshrc', 'fabfile.py']:
        link_path = '~/{link}'.format(link=filename)
        if is_link(link_path):
            local('rm {link_path}'.format(link_path=link_path))
        file_path = '{curr_dir}/files/{filename}'.format(curr_dir=CURR_DIR, filename=filename)
        local('ln -s {file_path} {link_path}'.format(file_path=file_path, link_path=link_path))

