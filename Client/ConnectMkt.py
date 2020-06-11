import socketio
import json
import logging
import time
sio = socketio.Client()
counter = 0

@sio.event
def __connect():
    print ("connection established")

@sio.event
def __disconnect():
    print ("disconnect from server")

@sio.event
def __my_message(data):
    sio.emit("my response", {'response':"my response"})

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
    hostname = "localhost"
    hostname = "ALB-t-907109132.us-east-2.elb.amazonaws.com"
    port = 80

    url = f"ws://{hostname}:{port}"
    sio.connect(url)

    subscribeMktData("AAPL 150117C00600000 EQUITY")

    time.sleep(60*10)

    sio.wait()