import logging
import argparse

from PyFlaskSocketIOServer.app import  app, socketio
from PyFlaskSocketIOServer.controller.healthcheck import httphealthCheck
from PyFlaskSocketIOServer.controller.authenticate import authenticate
from PyFlaskSocketIOServer.controller.ping import initMarketData




FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port number", type=int, default="80", required=True)
    args = parser.parse_args()
    port = args.port

    initMarketData()
    print(f"Running at port {port}")
    socketio.run(app, host="0.0.0.0", port=port)
