"""
Simple Backup.
"""
import os
from datetime import datetime
from fabric.api import task, hosts, local, env, settings
from fabric.colors import magenta
from fabric.context_managers import lcd
from decorator import decorator

env.hosts = ['web']
env.user = 'ahernp'


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


def rsync(source, dest):
    """Two-way rsync."""
    command = 'rsync -auvp --exclude \'*.pyc\' --stats --modify-window=1 %s/ %s' % (source, dest)
    print('Running \'%s\'' % (command))
    local(command)
    command = 'rsync -auv --stats --modify-window=1 %s/ %s' % (dest, source)
    print('Running \'%s\'' % (command))
    local(command)


@task
@hosts('localhost')
@timer
def backup():
    """Simple backup of local directories to USB drive."""
    for disk in ['SANDISK', '8B88-583A', 'HP v165w']:
        if os.path.exists('/media/ahernp/%s/work' % disk):
            rsync('~/Documents', '"/media/ahernp/%s/Documents"' % disk)
            rsync('~/Desktop/work', '"/media/ahernp/%s/work"' % disk)


@task
@hosts('localhost')
@timer
def full_backup():
    """Backup local directories."""
    def backup(directory):
        source = '/home/ahernp/%s/' % (directory)
        dest = '/media/ahernp/Iomega HDD/archive/%s' % (directory)
        print('# Backing up newer versions of files in %s to %s' % (source, dest))
        local('rsync -auv --stats --modify-window=1 --delete "%s" "%s"' % (source, dest))

    backup('Desktop/work')
    backup('Documents')
    #backup('dos')
    backup('ebooks')
    backup('Music')
    backup('Pictures')
    backup('Spoken')
    #backup('Videos')


@task
@hosts('localhost')
def check_git_status():
    """Check status of all local repositories."""
    REPOSITORIES = ['django-bugtracker', 'django-monitoring',
                    'config', 'django-ahernp',
                    'django-dmcm', 'django-feedreader']
    for repository in REPOSITORIES:
        with lcd('/home/ahernp/code/%s' % (repository)):
            local('pwd')
            local('git status')
