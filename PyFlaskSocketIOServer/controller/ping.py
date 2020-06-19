from PyFlaskSocketIOServer.app import socketio
from flask_socketio import emit
from flask import request
import json

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

@socketio.on("//blp/mktdata")
def handle_marketdataSubscription(mktDataRequest):
    #not working with flask websocket.... lost the session when callback by thread
    #def consumerFunc(msg):
    #    emit("//blp/mktdata/response", json.dumps(msg))

    clientId = request.sid
    if "mktdatacode" not in mktDataRequest:
        raise Exception ("mktdatacode not found in market data request")
    emit("//blp/mktdata/response", json.dumps(
        marketDataInterface.pollMarketData(mktDataRequest["mktdatacode"])
    ))
    #marketDataInterface.subscribe(
    #    clientId, mktDataRequest, consumerFunc
    #)
