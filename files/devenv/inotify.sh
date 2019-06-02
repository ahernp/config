#!/bin/sh
flake8 --append-config=/root/setup.cfg /work/ahernp.com

while inotifywait --recursive -e modify /work; do
    flake8 --append-config=/root/setup.cfg /work
done
