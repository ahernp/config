FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip ctags vim silversearcher-ag tzdata nodejs npm git

COPY ./ /root/
RUN pip3 install --upgrade pip
RUN pip3 install -r /root/requirements.txt

RUN mkdir /work
WORKDIR /work
