FROM node:9-alpine

RUN mkdir /app
WORKDIR /app

COPY package-lock.json package.json /app/
RUN npm install

COPY . /app
RUN npm run build
