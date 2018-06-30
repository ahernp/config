FROM python:3.7.0b5

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y inotify-tools ctags vim silversearcher-ag

COPY ./ /root/
RUN pip3 install -r /root/requirements.txt

RUN mkdir /work
WORKDIR /work

EXPOSE 8000
