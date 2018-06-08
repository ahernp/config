alias ls='ls -Fh --color=auto'
alias tag='ctags -R --fields=+l --languages=python --python-kinds=-iv -f ./tags $(python -c "import os, sys; print(\" \".join(\"{}\".format(d) for d in sys.path if os.path.isdir(d)))") ./'

grep "alias " /root/.bashrc
