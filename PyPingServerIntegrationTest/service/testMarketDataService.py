import unittest
from PyMktData.model.Observer import MktDataObserver
from PyMktData.model.Subject import MarketDataSubject
from PyMktData.service.marketDataService import DummyMarkDataImpl
import logging
from collections import deque
import time
import json
from utilities.container import BlockingQueue
import queue


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)



class MarketDataServiceSuite(unittest.TestCase):


    def test_insertSubject(self):
        marketDataInterface = DummyMarkDataImpl()
        marketDataInterface.connect()
        mktdatacode = "AAPL 150117C00600000 EQUITY"
        mktDataRequest = {}
        mktDataRequest["mktdatacode"]  = mktdatacode

        msgQueue = deque()

        def consumerFunc(msg):
            msgQueue.append(msg)

        def throwFunc(msg):
            print("throw:" + msg)
        marketDataInterface.subscribe("abcd", mktDataRequest, consumerFunc)
        marketDataInterface.subscribe("def", mktDataRequest, consumerFunc)
        time.sleep(6)

        marketDataInterface.disconnect()
        self.assertGreaterEqual(len(msgQueue), 4)
        logging.info(f"number of messages {len(msgQueue)}")


    def test_Streaming(self):
        marketDataInterface = DummyMarkDataImpl()
        marketDataInterface.connect()
        mktdatacode = "AAPL 150117C00600000 EQUITY"
        mktDataRequest = {}
        mktDataRequest["mktdatacode"] = mktdatacode


        blockingQueue = BlockingQueue()
        marketDataInterface.subscribe("abcd", mktDataRequest, blockingQueue.insertItem)

        counter = 0
        while (True):
            try:
                msg = blockingQueue.consumeItem(1)
                print(json.dumps(msg))
                counter += 1

                if counter>10:
                    break
            except Exception as ex:
                if ex.__class__.__name__ == "Empty":
                    print(ex)
                else:
                    raise ex

        marketDataInterface.disconnect()

