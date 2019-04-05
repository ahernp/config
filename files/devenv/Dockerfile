FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3 python3-pip ctags vim silversearcher-ag

COPY ./ /root/
RUN pip3 install -r /root/requirements.txt

RUN mkdir /work
WORKDIR /work

EXPOSE 8000
