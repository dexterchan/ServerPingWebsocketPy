from PyPingServer.app import socketio
from flask_socketio import send, emit
from flask import request
import json

@socketio.on("connect")
def connect():
    header=request.headers
    print(f'connection established {header}')
    if ("user" not in header):
        raise ConnectionRefusedError('unauthorized!')

@socketio.on("disconnect")
def connect():
    print('disconnect')

@socketio.on("//blp/mktdata")
def handle_marketdataSubscription(mktRequest):
    emit ("//blp/mktdata/response", json.dumps(
        {
            "bid":123,
            "ask":122
        }
        )
    )