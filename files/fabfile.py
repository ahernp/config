from datetime import datetime
from pytz import timezone
import getpass
import os
from fabric.api import task, hosts, local, env
from fabric.colors import yellow
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
    rsync("~/code/pmcm/data", "~/Desktop/work/pmcm/data")
    rsync("~/code/pmcm/media", "~/Desktop/work/pmcm/media")
    local(
        "find ~/Documents/accounts -type f -mtime +3 -exec rm {} \;"
    )  # delete old accounts files

    disk_found = False
    for disk in ["Kingston", "hp"]:
        if os.path.exists("/media/%s/%s/work" % (current_userid, disk)):
            disk_found = True
            rsync("~/Documents", '"/media/%s/%s/Documents"' % (current_userid, disk))
            rsync("~/Desktop/work", '"/media/%s/%s/work"' % (current_userid, disk))
            rsync(
                '"/media/%s/%s/work"' % (current_userid, disk), "~/Desktop/work"
            )  # Copy changes from disk
            break
    if not disk_found:
        print(yellow("Error no disk found for backup"))
        return

    # Restore permissions on private keys
    local("chmod o-rx,g-rx ~/.ssh/github/id_rsa")
    local("chmod o-rx,g-rx ~/.ssh/id_rsa")

    rsync("~/Desktop/work/pmcm/data", "~/code/pmcm/data")
    rsync("~/Desktop/work/pmcm/media", "~/code/pmcm/media")


@task
@hosts("localhost")
def full_backup():
    """Backup of more directories to USB drive."""
    rsync("~/Desktop/work", '"/media/ahernp/Iomega\ HDD/archive/work/affectv"')
    for directory in ["Documents", "ebooks", "Music", "Pictures", "Spoken"]:
        rsync("~/%s" % directory, "/media/ahernp/Iomega\ HDD/archive/%s" % directory)


@task
@hosts("localhost")
def check_git_status():
    """Check status of all local repositories."""
    REPOSITORIES = ["ahernp.com", "config", "pmcm"]
    for repository in REPOSITORIES:
        with lcd("/home/%s/code/%s" % (current_userid, repository)):
            local("pwd")
            local("git status")


@task
@hosts("localhost")
def times():
    """Show current time in various timezones"""
    TIMEZONES = [
        "America/Los_Angeles",
        "America/New_York",
        "Europe/London",
        "Asia/Singapore",
        "Australia/Sydney",
    ]

    for tz_str in TIMEZONES:
        tz = timezone(tz_str)
        time = datetime.now(tz)
        print("%s (%s)" % (time.strftime('%Y-%m-%d %H:%M:%S'), tz_str))
