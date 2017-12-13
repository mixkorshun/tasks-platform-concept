FROM python:3.5-slim

RUN mkdir /app
WORKDIR /app

RUN apt-get -qq update \
    && apt-get -qq -y install gcc libmysqlclient-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install mysqlclient

RUN apt-get -qq update \
    && apt-get -qq -y install netcat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn gevent

RUN pip install mysqlclient

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x wait_for_database.sh

CMD ./wait_for_database.sh && gunicorn -b 0.0.0.0:80 -k gevent -w 4 wsgi_gevent:app
