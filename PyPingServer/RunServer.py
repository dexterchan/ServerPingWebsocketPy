import logging
import argparse

from PyPingServer.app import  app, socketio
from PyPingServer.controller.healthcheck import httphealthCheck
from PyPingServer.controller.authenticate import authenticate
from PyPingServer.controller.ping import initMarketData




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
