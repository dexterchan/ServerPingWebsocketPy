#!/bin/bash
rm -Rf dist
python3 setup.py sdist

docker build --tag pigpiggcp/serverpingwebsocket:v0.py .
docker push pigpiggcp/serverpingwebsocket:v0.py