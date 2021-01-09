from datetime import datetime
from pytz import timezone
import getpass
import os
from fabric import Connection, task
from rich import print

current_userid = getpass.getuser()

local = Connection("localhost")


def rsync(source, dest):
    """Copy files from source to destination.."""
    source += "/"
    command = "rsync -auv --exclude '*.pyc' --stats --modify-window=1 %s %s" % (
        source,
        dest,
    )
    print("Running '%s'" % (command))
    local.run(command)


@task
def backup(local):
    """Simple backup of local directories to USB drive."""
    rsync("~/code/pmcm/data", "~/Desktop/work/pmcm/data")
    rsync("~/code/pmcm/media", "~/Desktop/work/pmcm/media")
    local.run(
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
        print("[blink yellow]Error no disk found for backup[/blink yellow]")
        return

    # Restore permissions on private keys
    local.run("chmod o-rx,g-rx ~/.ssh/github/id_rsa")
    local.run("chmod o-rx,g-rx ~/.ssh/id_rsa")

    rsync("~/Desktop/work/pmcm/data", "~/code/pmcm/data")
    rsync("~/Desktop/work/pmcm/media", "~/code/pmcm/media")


@task
def full_backup(local):
    """Backup of more directories to USB drive."""
    rsync("~/Desktop/work", "/media/ahernp/Iomega\ HDD/archive/work/affectv")
    for directory in ["Documents", "ebooks", "Music", "Pictures"]:
        rsync("~/%s" % directory, "/media/ahernp/Iomega\ HDD/archive/%s" % directory)


@task
def times(local):
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
