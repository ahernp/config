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
        print("{command} {e}".format(command=command, e=e))


def setup_dot_ssh():
    print("Setup .ssh:")
    home_dot_ssh = "{home_dir}/.ssh".format(home_dir=HOME_DIR)
    work_dot_ssh_path = "{home_dir}/Desktop/work/dot.ssh".format(home_dir=HOME_DIR)

    if os.path.isdir(home_dot_ssh):
        print("{home_dot_ssh} already exists".format(home_dot_ssh=home_dot_ssh))
    if not os.path.isdir(work_dot_ssh_path):
        print(
            "{work_dot_ssh_path} does not exist".format(
                work_dot_ssh_path=work_dot_ssh_path
            )
        )

    if not os.path.isdir(home_dot_ssh) and os.path.isdir(work_dot_ssh_path):
        run("mkdir {home_dot_ssh}".format(home_dot_ssh=home_dot_ssh))
        run(
            "cp -r {work_dot_ssh_path}/* {home_dot_ssh}".format(
                work_dot_ssh_path=work_dot_ssh_path, home_dot_ssh=home_dot_ssh
            )
        )

        run("chmod g-rx,o-rx {home_dir}/.ssh/github/id_rsa".format(home_dir=HOME_DIR))
        run("chmod g-rx,o-rx {home_dir}/.ssh/id_rsa".format(home_dir=HOME_DIR))


def apt_install():
    print("Install apt packages:")
    APT_PACKAGES = [
        "byobu",
        "calibre",
        "curl",
        "docker.io",
        "docker-compose",
        "fabric",
        "geany",
        "geany-plugins",
        "git",
        "gnucash",
        "htop",
        "hunspell-en-gb",
        "screen",
        "silversearcher-ag",
        "speedcrunch",
        "ssh",
        "tree",
        "vim",
        "vlc",
        "zsh",
    ]
    run("sudo apt install {packages}".format(packages=" ".join(APT_PACKAGES)))


def add_home_configs():
    print("Add configuration files to home directory:")
    for filename in [".gitconfig", ".vimrc", ".zshrc", "fabfile.py"]:
        link_path = "{home_dir}/{link}".format(home_dir=HOME_DIR, link=filename)
        run("rm {link_path}".format(link_path=link_path))
        run(
            "ln -s {curr_dir}/files/{filename} {link_path}".format(
                curr_dir=CURR_DIR, filename=filename, link_path=link_path
            )
        )
    run("rm {home_dir}/.zsh_history".format(home_dir=HOME_DIR))
    run(
        "cp {curr_dir}/files/.zsh_history {home_dir}/.zsh_history".format(
            curr_dir=CURR_DIR, home_dir=HOME_DIR
        )
    )


def setup_vim():
    print("Setup vim:")
    run(
        "git clone https://github.com/VundleVim/Vundle.vim {home_dir}/.vim/bundle/vundle.vim "
        "|| cd {home_dir}/.vim/bundle/vundle.vim; git pull".format(home_dir=HOME_DIR)
    )
    run(
        "git clone https://github.com/leafgarland/typescript-vim.git {home_dir}/.vim/bundle/typescript-vim.vim "
        "|| cd {home_dir}/.vim/bundle/typescript-vim.vim; git pull".format(
            home_dir=HOME_DIR
        )
    )

    run("rm {home_dir}/.vim/colors".format(home_dir=HOME_DIR))
    run(
        "ln -s {curr_dir}/files/.vim/colors {home_dir}/.vim/colors".format(
            curr_dir=CURR_DIR, home_dir=HOME_DIR
        )
    )
    run("vim +BundleInstall +qall")


def setup_byobu():
    print("Setup byobu")
    run("byobu-select-backend screen")
    run(
        "cp {curr_dir}/files/byobu.desktop "
        "{home_dir}/.local/share/applications/byobu.desktop".format(
            curr_dir=CURR_DIR, home_dir=HOME_DIR
        )
    )


def setup_vcprompt():
    print("Setup vcprompt:")
    run(
        "sudo ln -s {curr_dir}/files/vcprompt /usr/local/bin/vcprompt".format(
            curr_dir=CURR_DIR
        )
    )


def setup_etc_hosts():
    print("Setup /etc/hosts:")
    run("sudo cp {curr_dir}/files/hosts /etc/hosts".format(curr_dir=CURR_DIR))
    run("sudo chmod u=rw,g=r,o=r /etc/hosts")


def change_shell_to_zsh():
    print("Change shell to zsh:")
    run("chsh -s /usr/bin/zsh")
    run(
        "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /tmp/zsh-syntax-highlighting"
    )
    run("sudo mv /tmp/zsh-syntax-highlighting /usr/local/share/zsh-syntax-highlighting")


def install_atom_ide():
    print("Install atom IDE:")
    run("curl -L https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -")
    run(
        'sudo sh -c \'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" '
        "> /etc/apt/sources.list.d/atom.list'"
    )
    run("sudo apt update")
    run("sudo apt install atom")


def setup_devenv():
    print("Setup development environment:")
    run(
        "ln -s {curr_dir}/files/devenv/docker-compose.yml "
        "{parent_dir}/docker-compose.yml".format(
            curr_dir=CURR_DIR, parent_dir=PARENT_DIR
        )
    )
    run(
        "ln -s {curr_dir}/files/devenv/.pylintrc {parent_dir}/.pylintrc".format(
            curr_dir=CURR_DIR, parent_dir=PARENT_DIR
        )
    )
    run(
        "ln -s {curr_dir}/files/devenv/setup.cfg {parent_dir}/setup.cfg".format(
            curr_dir=CURR_DIR, parent_dir=PARENT_DIR
        )
    )
    run(
        "ln -s {curr_dir}/files/devenv {parent_dir}/devenv".format(
            curr_dir=CURR_DIR, parent_dir=PARENT_DIR
        )
    )


def main():
    setup_dot_ssh()
    proceed = input("Check ~/.ssh has been setup. Proceed (y/n): ")
    if proceed == "y":
        apt_install()
        add_home_configs()
        setup_vim()
        setup_byobu()
        setup_vcprompt()
        setup_etc_hosts()
        change_shell_to_zsh()
        install_atom_ide()
        setup_devenv()


if __name__ == "__main__":
    main()
