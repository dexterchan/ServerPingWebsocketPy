import socketio
import json
import logging
import uuid
import time
sio = socketio.Client(reconnection=True)
counter = 0
import argparse

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
        "sessionid" : str(uuid.uuid4()),
        "mktdatacode": mktdatacode,
        "fields": ["BID", "ASK"]
    }
    global sio
    sio.emit("//blp/mktdata", mktRequest)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--location", help="hostname:port", type=str, default="localhost:80", required=True)
    args = parser.parse_args()
    location = args.location

    url = f"{location}"
    sio.connect(url, headers={"user":"pigpig", "token":"abcd"})

    subscribeMktData("AAPL 150117C00600000 EQUITY")
    subscribeMktData("AMZN 150117C00600000 EQUITY")
    subscribeMktData("MSFT 150117C00600000 EQUITY")
    time.sleep(60*10)

    sio.wait()