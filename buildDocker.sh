#!/bin/bash
rm -Rf dist
python3 setup.py sdist

VERSION=v1
docker build --tag pigpiggcp/serverpingwebsocket:$VERSION.py .
docker push pigpiggcp/serverpingwebsocket:$VERSION.py