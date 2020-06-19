from aiohttp import web
import socketio
from flask import Flask
app = Flask(__name__)
import json

sio = socketio.Server(async_mode='eventlet')

# Creates a new Aiohttp Web Application
# wrap with a WSGI application
app = socketio.WSGIApp(sio)



# we can define aiohttp endpoints just as we normally
# would with no change
def index(request):
    return web.Response(text="OK", content_type='text/html')

# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
@sio.on('message')
def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    print("1) Socket ID: " , sid)
    print(message)
    sio.emit("myresponse", "Hello!")

@sio.on('clientresponse')
def clientresponse_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    print("2) Socket ID: " , sid)
    print(message)

# We bind our aiohttp endpoint to our app
# router
#app.router.add_get('/', index)



from PyMktData.service.marketDataService import DummyMarkDataImpl

marketDataInterface = None

def initMarketData():
    global marketDataInterface
    marketDataInterface = DummyMarkDataImpl()
    marketDataInterface.connect()



@sio.on("//blp/mktdata")
def handle_marketdataSubscription(sid, mktDataRequest):
    #not working with flask websocket.... lost the session when callback by thread


    def sioconsumerFunc(msg):
        sio.emit("//blp/mktdata/response", json.dumps(msg))

    clientId = sid
    if "mktdatacode" not in mktDataRequest:
        raise Exception ("mktdatacode not found in market data request")



    #marketDataInterface.subscribe(
    #    clientId, mktDataRequest, sioconsumerFunc
     #)

# We kick off our server
if __name__ == '__main__':
    port = 3000
    initMarketData()
    app = socketio.WSGIApp(sio)
    import eventlet

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)