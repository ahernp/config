Configure Local PC
==================

Directory ~/Desktop/work/dot.ssh must exist on the PC.

1. sudo apt install ansible
2. sudo echo "localhost" >> /etc/ansible/hosts
3. cd ~/code/config/setup_pc
4. ansible-playbook -K local.yml
