"""
Simple Backup.
"""
import getpass
import os
from datetime import datetime
from fabric.api import task, hosts, local, env, settings
from fabric.colors import magenta
from fabric.context_managers import lcd
from decorator import decorator

current_userid = getpass.getuser()

env.hosts = ['web']
env.user = current_userid


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
    """Copy files from source to destination.."""
    command = 'rsync -auvp --exclude \'*.pyc\' --stats --modify-window=1 %s/ %s' % (source, dest)
    print('Running \'%s\'' % (command))
    local(command)


@task
@hosts('localhost')
@timer
def backup():
    """Simple backup of local directories to USB drive."""
    local('find ~/Documents/accounts -type f -mtime +3 -exec rm {} \;')  # delete old accounts files
    for disk in ['KINGSTON', '8B88-583A', 'E32B-3BF2']:
        if os.path.exists('/media/%s/%s/work' % (current_userid, disk)):
            rsync('~/Documents', '"/media/%s/%s/Documents"' % (current_userid, disk))
            rsync('~/Desktop/work', '"/media/%s/%s/work"' % (current_userid, disk))
            rsync('"/media/%s/%s/work"' % (current_userid, disk), '~/Desktop/work')  # Copy changes from disk
            break

    # Restore permissions on private keys
    local('chmod o-rx ~/.ssh/github/id_rsa')
    local('chmod g-rx ~/.ssh/github/id_rsa')
    local('chmod o-rx ~/.ssh/id_rsa')
    local('chmod g-rx ~/.ssh/id_rsa')


@task
@hosts('localhost')
@timer
def full_backup():
    """Backup local directories."""
    def backup(directory):
        source = '/home/%s/%s/' % (current_userid, directory)
        for disk in ['KINGSTON', 'Iomega HDD']:
            if os.path.exists('/media/%s/%s/archive/Desktop/work' % (current_userid, disk)):
                dest = '/media/%s/%s/archive/%s' % (current_userid, disk, directory)
                print('# Backing up newer versions of files in %s to %s' % (source, dest))
                local('rsync -auvp --stats --modify-window=1 --delete "%s" "%s"' % (source, dest))
                break

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
    REPOSITORIES = ['ahernp', 'angular-django', 'config']
    for repository in REPOSITORIES:
        with lcd('/home/%s/code/%s' % (current_userid, repository)):
            local('pwd')
            local('git status')
