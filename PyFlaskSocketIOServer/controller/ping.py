from PyFlaskSocketIOServer.app import socketio
from flask_socketio import emit
from flask import request
import json
import eventlet

from PyMktData.service.marketDataService import DummyMarkDataImpl

marketDataInterface = None

def initMarketData():
    global marketDataInterface
    marketDataInterface = DummyMarkDataImpl()
    marketDataInterface.connect()

@socketio.on("connect")
def connect():
    header=request.headers
    print(f'connection established {header}')
    if ("user" not in header):
        raise ConnectionRefusedError('unauthorized!')

@socketio.on("disconnect")
def connect():
    print('disconnect')

def flushStreamData(sio, channel, msg):
    sio.emit(channel, msg)
    eventlet.sleep(0)

@socketio.on("//blp/mktdata")
def handle_marketdataSubscription(mktDataRequest):
    #not working with flask websocket.... lost the session when callback by thread

    consumerFunc = lambda sio: lambda msg: flushStreamData(sio, "//blp/mktdata/response", json.dumps(msg))

    clientId = request.sid
    if "mktdatacode" not in mktDataRequest:
        raise Exception ("mktdatacode not found in market data request")

    sioconsumerFunc = consumerFunc(socketio)
    #sioconsumerFunc(marketDataInterface.pollMarketData(mktDataRequest["mktdatacode"]))

    #marketDataInterface.subscribe(
    #    clientId, mktDataRequest, sioconsumerFunc
    #)
    import time
    import random
    cnt = 0
    while (True):
        cnt += 1
        msg = {
            "Bid": random.random() * (10-1) + 1,
            "Ask": random.random() * (10-1) + 1
        }
        sioconsumerFunc(json.dumps(msg))
        time.sleep(1)
