FROM node:9-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache nginx
RUN mkdir /run/nginx

COPY package-lock.json package.json /app/
RUN npm install

COPY src/ /app/src/
COPY webpack.config.js /app

RUN npm run build:optimize

COPY nginx.conf /etc/nginx

EXPOSE 80
STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
