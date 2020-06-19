
import socketio
import json
import logging
import time

sio = socketio.Client(reconnection=True)
counter = 0

@sio.event
def __connect():
    print ("connection established")

@sio.event
def __disconnect():
    print ("disconnect from server")


@sio.on("myresponse")
def __myresponse(data):
    print(data)
    sio.emit("clientresponse", {'response':"my response"})

@sio.on("//blp/mktdata/response")
def __mktdataresponse(data):
    global counter
    counter += 1
    print ("receive mkt data:", data)

def subscribeMktData(mktdatacode:str):
    mktRequest = {
        "mktdatacode": mktdatacode,
        "fields": ["BID", "ASK"]
    }
    global sio
    sio.emit("//blp/mktdata", mktRequest)


if __name__ == "__main__":
        location="localhost:3000"
        url = f"ws://{location}"
        sio.connect(url, headers={"user": "pigpig", "token": "abcd"})

        #sio.emit("message", "Hello from client!")
        subscribeMktData("AAPL 150117C00600000 EQUITY")

        #time.sleep(60 * 10)

        sio.wait()