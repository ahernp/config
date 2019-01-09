#!/bin/sh
flake8 --append-config=/root/setup.cfg /work/ahernp.com
pylint --rcfile=/root/.pylintrc /work/ahernp.com

while inotifywait --recursive -e modify /work; do
    flake8 --append-config=/root/setup.cfg /work
    pylint --rcfile=/root/.pylintrc /work
done
