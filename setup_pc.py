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


def apt_install():
    print("Install apt packages:")
    APT_PACKAGES = [
        "bat",
        "black",
        "btop",
        "calibre",
        "curl",
        "epiphany-browser",
        "fabric",
        "geany",
        "geany-plugins",
        "git",
        "gnucash",
        "htop",
        "inkscape",
        "kitty",
        "locate",
        "ncal",
        "neofetch",
        "python3-pip",
        "python3-pylsp",
        "python3-venv",
        "qalculate-gtk",
        "ranger",
        "silversearcher-ag",
        "tldr",
        "tree",
        "ufw",
        "vlc",
        "zsh",
    ]
    run(f"apt install {' '.join(APT_PACKAGES)}")


def setup_etc_hosts():
    print("Setup /etc/hosts:")
    run(f"cp {CURR_DIR}/files/hosts /etc/hosts")
    run("chmod u=rw,g=r,o=r /etc/hosts")


def install_zsh_syntax_highlighting():
    print("Install zsh syntax highlighting:")
    run(
        "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /tmp/zsh-syntax-highlighting"
    )
    run("mv /tmp/zsh-syntax-highlighting /usr/local/share/zsh-syntax-highlighting")


def enable_firewall():
    print("Enable Firewall:")
    run("ufw enable")


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


def add_home_configs():
    print("Add configuration files to home directory:")
    for filename in [".gitconfig", ".zshrc", "fabfile.py"]:
        link_path = f"{HOME_DIR}/{filename}"
        run(f"rm {link_path}")
        run(f"ln -s {CURR_DIR}/files/{filename} {link_path}")
    run(f"rm {HOME_DIR}/.zsh_history")
    run(f"cp {CURR_DIR}/files/.zsh_history {HOME_DIR}/.zsh_history")


def add_kitty_config():
    print("Add configuration files for kitty:")
    run(f"mkdir -p {HOME_DIR}/.config/kitty")
    for filename in ["kitty", "ahernp-kitty", "current-theme", "ahernp-session"]:
        run(
            f"ln -s {CURR_DIR}/files/kitty/{filename}.conf {HOME_DIR}/.config/kitty/{filename}.conf"
        )


def add_helix_config():
    print("Add configuration files for helix:")
    run(f"mkdir -p {HOME_DIR}/.config/helix/themes")
    for filename in ["config", "languages", "themes/ahernp"]:
        run(
            f"ln -s {CURR_DIR}/files/helix/{filename}.toml {HOME_DIR}/.config/helix/{filename}.toml"
        )


def install_rust():
    print("Install rust cargo and packages:")
    run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    run("cargo install --git https://github.com/XAMPPRocky/tokei.git tokei")
    run("cargo install ripgrep")
    run("cargo install repgrep")
    run("cargo install --locked serie")
    run("cargo install --locked yazi-fm yazi-cli")


def change_shell_to_zsh():
    print("Change shell to zsh:")
    run("chsh -s /usr/bin/zsh")


def main():
    is_root = os.geteuid() == 0
    if is_root:
        apt_install()
        setup_etc_hosts()
        install_zsh_syntax_highlighting()
        enable_firewall()
    else:
        setup_dot_ssh()
        add_helix_config()
        add_kitty_config()
        install_rust()
        proceed = input("Check ~/.ssh has been set up. Proceed (y/n): ")
        if proceed == "y":
            add_home_configs()
            change_shell_to_zsh()


if __name__ == "__main__":
    main()
