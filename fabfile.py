"""
Setup Ubuntu PC.
"""
from fabric.contrib.files import is_link

import os
from datetime import datetime
from fabric.api import task, hosts, local, env, settings
from fabric.colors import magenta
from fabric.context_managers import lcd
from decorator import decorator

@decorator
def timer(func, *args, **kwargs):
    """Wrapper which outputs how long a function took to run."""
    start_time = datetime.now()
    result = func(*args, **kwargs)
    end_time = datetime.now()
    duration = end_time - start_time
    print(magenta('\n# \'{}\' ran for {} (started at {:%H:%M:%S}, '
                  'ended at {:%H:%M:%S})'.format(
                      func.__name__,
                      duration,
                      start_time,
                      end_time)))
    return result

@task
@hosts('localhost')
@timer
def setup_pc():
    """Setup Development PC."""
    VIMRC_LINK = '~/Desktop/vimrc'
    VIMRC_FILE = '~/code/config/ansible/setup_pc/roles/devpc/files/.vimrc'
    if is_link(VIMRC_LINK):
        local('rm {link}'.format(link=VIMRC_LINK))
    local('ln -s {file} {link}'.format(file=VIMRC_FILE, link=VIMRC_LINK))  # Create link to vim configuration file

