"""
Simple Backup.
"""
import getpass
import os
from fabric.api import task, hosts, local, env
from fabric.context_managers import lcd

current_userid = getpass.getuser()

env.hosts = ["web"]
env.user = current_userid


def rsync(source, dest):
    """Copy files from source to destination.."""
    command = "rsync -auvp --exclude '*.pyc' --stats --modify-window=1 %s/ %s" % (
        source,
        dest,
    )
    print("Running '%s'" % (command))
    local(command)


@task
@hosts("localhost")
def backup_dmcm():
    """ Backup text and files from dmcm """
    with lcd("/home/%s/code/dmcm" % (current_userid)):
        local("docker-compose exec webapp python manage.py delete_logs")
        local("docker-compose exec webapp python manage.py delete_page_reads")
        local(
            "docker-compose exec webapp python manage.py dumpdata --indent 4 core mpages timers > ~/Desktop/work/dmcm/snapshot.json"
        )
    local("sudo chown {user}:{user} -R ~/code/dmcm".format(user=current_userid))
    rsync("~/code/dmcm/media", "~/Desktop/work/dmcm/media")


@task
@hosts("localhost")
def restore_dmcm():
    """ Restore text and files in dmcm from backup """
    rsync("~/Desktop/work/dmcm/media", "~/code/dmcm/media")
    local("cp ~/Desktop/work/dmcm/snapshot.json ~/code/dmcm/snapshot.json")
    with lcd("/home/%s/code/dmcm" % (current_userid)):
        local("docker-compose exec webapp python manage.py loaddata snapshot.json")
    local("rm ~/code/dmcm/snapshot.json")


@task
@hosts("localhost")
def backup():
    """Simple backup of local directories to USB drive."""
    local(
        "find ~/Documents/accounts -type f -mtime +3 -exec rm {} \;"
    )  # delete old accounts files

    for disk in ["KINGSTON", "hp"]:
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


@task
@hosts("localhost")
def full_backup():
    """Backup local directories."""

    def backup(directory):
        source = "/home/%s/%s/" % (current_userid, directory)
        for disk in ["KINGSTON", "Iomega HDD"]:
            if os.path.exists(
                "/media/%s/%s/archive/Desktop/work" % (current_userid, disk)
            ):
                dest = "/media/%s/%s/archive/%s" % (current_userid, disk, directory)
                print(
                    "# Backing up newer versions of files in %s to %s" % (source, dest)
                )
                local(
                    'rsync -auvp --stats --modify-window=1 --delete "%s" "%s"'
                    % (source, dest)
                )
                break

    backup("Desktop/work")
    backup("Documents")
    backup("ebooks")
    backup("Music")
    backup("Pictures")
    backup("Spoken")


@task
@hosts("localhost")
def check_git_status():
    """Check status of all local repositories."""
    REPOSITORIES = ["ahernp.com", "config", "dmcm"]
    for repository in REPOSITORIES:
        with lcd("/home/%s/code/%s" % (current_userid, repository)):
            local("pwd")
            local("git status")
