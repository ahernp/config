#!/bin/sh
flake8 --append-config=/root/setup.cfg /work
pylint --rcfile=/root/.pylintrc /work

while inotifywait --recursive -e modify /work; do
    flake8 --append-config=/root/setup.cfg /work
    pylint --rcfile=/root/.pylintrc /work
done
