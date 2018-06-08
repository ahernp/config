FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y inotify-tools ctags vim

COPY ./* /root/
RUN pip3 install -r /root/requirements.txt

RUN mkdir /work
WORKDIR /work
