from datetime import datetime
from pytz import timezone
import getpass
import os
from fabric import task
from rich import print

current_userid = getpass.getuser()


def rsync(context, source, dest):
    """Copy files from source to destination.."""
    source += "/"
    command = (
        "rsync -auv --exclude '*.pyc' --stats --modify-window=1 %s %s | grep 'files transferred'"
        % (
            source,
            dest,
        )
    )
    print("Running '%s'" % (command))
    context.run(command)


@task
def backup(local):
    """Simple backup of local directories to USB drive."""
    rsync(local, "~/code/pmcm/data", "~/Desktop/work/pmcm/data")
    rsync(local, "~/code/pmcm/media", "~/Desktop/work/pmcm/media")
    local.run(
        r"find ~/Documents/accounts -type f -mtime +3 -exec rm {} \;"
    )  # delete old accounts files

    disk_found = False
    for disk in ["Kingston", "HP"]:
        if os.path.exists("/media/%s/%s/work" % (current_userid, disk)):
            disk_found = True
            rsync(
                local,
                "~/Documents",
                '"/media/%s/%s/Documents"' % (current_userid, disk),
            )
            rsync(
                local, "~/Desktop/work", '"/media/%s/%s/work"' % (current_userid, disk)
            )
            rsync(
                local, '"/media/%s/%s/work"' % (current_userid, disk), "~/Desktop/work"
            )  # Copy changes from disk
            break
    if not disk_found:
        print("[blink yellow]Error no disk found for backup[/blink yellow]")
        return

    # Restore permissions on private keys
    local.run("chmod o-rx,g-rx ~/.ssh/github/id_rsa")
    local.run("chmod o-rx,g-rx ~/.ssh/id_rsa")

    rsync(local, "~/Desktop/work/pmcm/data", "~/code/pmcm/data")
    rsync(local, "~/Desktop/work/pmcm/media", "~/code/pmcm/media")


@task
def full_backup(local):
    """Backup of more directories to USB drive."""
    rsync(local, "~/Desktop/work", r"/media/ahernp/Iomega\ HDD/archive/work/affectv")
    for directory in ["Documents", "ebooks", "Music", "Pictures"]:
        rsync(
            local,
            "~/%s" % directory,
            r"/media/ahernp/Iomega\ HDD/archive/%s" % directory,
        )


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
        print("%s (%s)" % (time.strftime("%Y-%m-%d %H:%M:%S"), tz_str))


@task
def numbers_of_days(local):
    """Numbers of days since and to various dates"""
    now = datetime.now()
    print(f'Today is {now.strftime("%a, %d %b %Y")}:')
    for target, label in [
        ("2020-02-01", "Brexit"),
        (f"{now.year}-12-25", "Christmas"),
    ]:
        target_date = datetime.strptime(target, "%Y-%m-%d")
        if target_date < now:
            number_of_days = (now - target_date).days
            label_prefix = "since"
        else:
            number_of_days = (target_date - now).days
            label_prefix = "to"
        print(f"{number_of_days:>8,} days {label_prefix} {label}")
