#!/bin/bash
if [ "$LOCATION" == "" ]
then
    LOCATION=ws://localhost:80
fi
export PYTHONPATH=.

python3 Client/ConnectMkt.py -l $LOCATION
