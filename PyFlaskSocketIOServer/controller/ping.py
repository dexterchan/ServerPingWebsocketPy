from PyFlaskSocketIOServer.app import socketio
from flask_socketio import emit
from flask import request
import json
import eventlet
import logging
import queue
from PyMktData.service.marketDataService import DummyMarkDataImpl

marketDataInterface = None

TIMEOUT_MKT_SEC=10

ClientMapALive = {}

def initMarketData():
    global marketDataInterface
    marketDataInterface = DummyMarkDataImpl()
    marketDataInterface.connect()

@socketio.on("connect")
def connect():
    header=request.headers
    clientId = request.sid
    ClientMapALive[clientId] = True
    print(f'connection established {header}')
    if ("user" not in header):
        raise ConnectionRefusedError('unauthorized!')

@socketio.on("disconnect")
def disconnect():
    clientId = request.sid
    if clientId in ClientMapALive:
        ClientMapALive[clientId] = False
    print('disconnect:' + clientId)


from utilities.container import BlockingQueue

def flushStreamData(sio, channel, msg):
    sio.emit(channel, msg)
    eventlet.sleep(0)

@socketio.on("//blp/mktdata")
def handle_marketdataSubscription(mktDataRequest):
    # Note: socket connection from front end thread cannot shared with other thread
    # If we send the sio to background thread,
    # the callback in background thread cannot connect to client anymore
    # therefore, we use blocking queue to pass data from background thread to frontend thread

    blockingQueue = BlockingQueue()
    clientId = request.sid
    if "mktdatacode" not in mktDataRequest:
        raise Exception ("mktdatacode not found in market data request")

    marketDataInterface.subscribe(
        clientId, mktDataRequest, blockingQueue.insertItem
    )
    if clientId not in ClientMapALive:
        raise Exception("client is not disconnected")

    while(ClientMapALive[clientId]):
        try:
            msg = blockingQueue.consumeItem(TIMEOUT_MKT_SEC)
            logging.info("publish data to "+clientId+":"+json.dumps(msg))
            flushStreamData(socketio,  "//blp/mktdata/response", json.dumps(msg))
        except queue.Empty as em:
            print(em)
        except Exception as ex:
            raise ex
    logging.info("market data disconnect Blocking queue released")