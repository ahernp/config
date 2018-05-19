FROM python:3-alpine

RUN mkdir /work
WORKDIR /work

COPY ./requirements.txt /work/
RUN pip3 install -r requirements.txt
