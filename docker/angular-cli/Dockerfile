FROM node:latest

ENV NPM_CONFIG_PREFIX=/home/node/.npm-global

WORKDIR /app

USER node

RUN npm install -g @angular/cli

ENV PATH="/home/node/.npm-global/bin:${PATH}"
