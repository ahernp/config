import getpass
import os
from fabric.api import task, hosts, local, env
from fabric.context_managers import lcd
from fabric.contrib.console import confirm

current_userid = getpass.getuser()

env.hosts = ["web"]
env.user = current_userid


def rsync(source, dest):
    """Copy files from source to destination.."""
    source += "/"
    command = "rsync -auv --exclude '*.pyc' --stats --modify-window=1 %s %s" % (
        source,
        dest,
    )
    print("Running '%s'" % (command))
    local(command)


@task
@hosts("localhost")
def backup():
    """Simple backup of local directories to USB drive."""
    rsync("~/code/gmcm/data", "~/Desktop/work/gmcm/data")
    rsync("~/code/gmcm/media", "~/Desktop/work/gmcm/media")
    local(
        "find ~/Documents/accounts -type f -mtime +3 -exec rm {} \;"
    )  # delete old accounts files

    for disk in ["Kingston", "hp"]:
        if os.path.exists("/media/%s/%s/work" % (current_userid, disk)):
            rsync("~/Documents", '"/media/%s/%s/Documents"' % (current_userid, disk))
            rsync("~/Desktop/work", '"/media/%s/%s/work"' % (current_userid, disk))
            rsync(
                '"/media/%s/%s/work"' % (current_userid, disk), "~/Desktop/work"
            )  # Copy changes from disk
            break

    # Restore permissions on private keys
    local("chmod o-rx,g-rx ~/.ssh/github/id_rsa")
    local("chmod o-rx,g-rx ~/.ssh/id_rsa")

    rsync("~/Desktop/work/gmcm/data", "~/code/gmcm/data")
    rsync("~/Desktop/work/gmcm/media", "~/code/gmcm/media")


@task
@hosts("localhost")
def check_git_status():
    """Check status of all local repositories."""
    REPOSITORIES = ["ahernp.com", "config", "gmcm"]
    for repository in REPOSITORIES:
        with lcd("/home/%s/code/%s" % (current_userid, repository)):
            local("pwd")
            local("git status")
