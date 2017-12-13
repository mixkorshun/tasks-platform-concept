#!/usr/bin/env bash

if [ $DATABASE_HOST ]
then
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 1
    done
fi
