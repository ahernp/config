"""
Simple Backup.
"""
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
    command = 'rsync -auv --exclude \'*.pyc\' --stats --modify-window=1 --delete %s/ %s' % (source, dest)
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
    CONFIG_FILES = ['~/.zshrc', '~/.vimrc', '/etc/hosts', '~/fabfile.py',
                    '~/.gitconfig', '~/code/dmcm/project/.gitignore']
    with lcd('/home/ahernp/'):
        for config_file in CONFIG_FILES:
            filename = config_file.split('/')[-1]
            local('cp -u %s ~/Desktop/work/doc/%s' % (config_file, filename))
            local('cp -u %s ~/code/config/%s' % (config_file, filename))
        local('cp -u ~/t.txt ~/Desktop/work/t.txt')
        with settings(warn_only=True):
            local('rm .goutputstream*')
    rsync('~/Documents', '/media/truecrypt1/documents')
    rsync('~/Desktop/work', '/media/truecrypt1/work')


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
    local('cp -u ~/archive.tar.bz2 /media/ahernp/Iomega\ HDD/archive.tar.bz2')
