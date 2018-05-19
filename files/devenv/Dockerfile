FROM python:3

RUN apt-get update && apt-get install -y inotify-tools

RUN mkdir /opt/devenv
COPY ./* /opt/devenv/
RUN pip3 install -r /opt/devenv/requirements.txt

RUN mkdir /work
WORKDIR /work
