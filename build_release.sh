#!/usr/bin/env bash

set -e

if [ $# -eq 0 ]
  then
    echo "Please provide build filename. Example: ./build_release.sh build.tar.gz"
    exit 1;
fi

cd ui
npm install
rm -Rf ./dist
npm run build:optimize
cd ..

tar -X .releaseignore -zcf $1 --exclude ./build_release.sh --exclude ./.releaseignore --exclude $1 . > /dev/null
