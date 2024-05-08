import os
import subprocess

HOME_DIR = os.environ.get("HOME")
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURR_DIR)


def run(command):
    try:
        print(command)
        subprocess.call(command, shell=True)
    except OSError as e:
        print(f"{command} {e}")


def setup_dot_ssh():
    print("Setup .ssh:")
    home_dot_ssh = f"{HOME_DIR}/.ssh"
    work_dot_ssh_path = f"{HOME_DIR}/Desktop/work/dot.ssh"

    if os.path.isdir(home_dot_ssh):
        print(f"{home_dot_ssh} already exists")
    if not os.path.isdir(work_dot_ssh_path):
        print(f"{work_dot_ssh_path} does not exist")

    if not os.path.isdir(home_dot_ssh) and os.path.isdir(work_dot_ssh_path):
        run(f"mkdir {home_dot_ssh}")
        run(f"cp -r {work_dot_ssh_path}/* {home_dot_ssh}")

        run(f"chmod g-rx,o-rx {HOME_DIR}/.ssh/github/id_rsa")
        run(f"chmod g-rx,o-rx {HOME_DIR}/.ssh/id_rsa")


def apt_install():
    print("Install apt packages:")
    APT_PACKAGES = [
        "black",
        "byobu",
        "calibre",
        "fabric",
        "geany",
        "geany-plugins",
        "git",
        "gnucash",
        "htop",
        "inkscape",
        "python3-pip",
        "python3-pylsp",
        "python3-venv",
        "ranger",
        "silversearcher-ag",
        "tree",
        "vlc",
        "zsh",
    ]
    run(f"sudo apt install {' '.join(APT_PACKAGES)}")


def add_home_configs():
    print("Add configuration files to home directory:")
    for filename in [".gitconfig", ".zshrc", "fabfile.py"]:
        link_path = f"{HOME_DIR}/{filename}"
        run(f"rm {link_path}")
        run(f"ln -s {CURR_DIR}/files/{filename} {link_path}")
    run(f"rm {HOME_DIR}/.zsh_history")
    run(f"cp {CURR_DIR}/files/.zsh_history {HOME_DIR}/.zsh_history")


def setup_byobu():
    print("Setup byobu:")
    run(
        f"cp {CURR_DIR}/files/byobu.desktop {HOME_DIR}/.local/share/applications/byobu.desktop"
    )


def setup_vcprompt():
    print("Setup vcprompt:")
    run(f"sudo ln -s {CURR_DIR}/files/vcprompt /usr/local/bin/vcprompt")


def setup_etc_hosts():
    print("Setup /etc/hosts:")
    run(f"sudo cp {CURR_DIR}/files/hosts /etc/hosts")
    run("sudo chmod u=rw,g=r,o=r /etc/hosts")


def change_shell_to_zsh():
    print("Change shell to zsh:")
    run("chsh -s /usr/bin/zsh")
    run(
        "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /tmp/zsh-syntax-highlighting"
    )
    run("sudo mv /tmp/zsh-syntax-highlighting /usr/local/share/zsh-syntax-highlighting")


def enable_firewall():
    print("Enable Firewall:")
    run("sudo ufw enable")


def pipx_install():
    print("Install pip packages:")
    run("pipx install Markdown pre-commit")


def remove_home_from_desktop():
    print("Remove home folder from Desktop:")
    run("gsettings set org.gnome.shell.extensions.desktop-icons show-home false")


def main():
    setup_dot_ssh()
    proceed = input("Check ~/.ssh has been set up. Proceed (y/n): ")
    if proceed == "y":
        apt_install()
        add_home_configs()
        setup_byobu()
        setup_vcprompt()
        setup_etc_hosts()
        change_shell_to_zsh()
        enable_firewall()
        pip_install()
        remove_home_from_desktop()


if __name__ == "__main__":
    main()
