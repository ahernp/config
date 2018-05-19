#!/bin/sh
while inotifywait --recursive -e modify /work; do
    flake8 --append-config=/opt/devenv/setup.cfg /work
    pylint --rcfile=/opt/devenv/.pylintrc /work
done
