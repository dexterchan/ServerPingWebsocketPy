#!/bin/bash
if [ "$PORT" == "" ]
then
    PORT=3000
fi
export PYTHONPATH=.
python3 PyFlaskSocketIOServer/RunServer.py -p ${PORT}