import unittest
from PyMktData.model.Observer import MktDataObserver
from PyMktData.model.Subject import MarketDataSubject
from PyMktData.service.marketDataService import DummyMarkDataImpl
import logging
from collections import deque
import time





FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class MarketDataServiceSuite(unittest.TestCase):


    def test_insertSubject(self):
        self.marketDataInterface = DummyMarkDataImpl()
        self.marketDataInterface.connect()
        mktdatacode = "AAPL 150117C00600000 EQUITY"
        mktDataRequest = {}
        mktDataRequest["mktdatacode"]  = mktdatacode

        msgQueue = deque()

        def consumerFunc(msg):
            msgQueue.append(msg)

        def throwFunc(msg):
            print("throw:" + msg)
        self.marketDataInterface.subscribe("abcd", mktDataRequest, consumerFunc)
        self.marketDataInterface.subscribe("def", mktDataRequest, consumerFunc)
        time.sleep(6)

        self.marketDataInterface.disconnect()
        self.assertGreaterEqual(len(msgQueue), 10)
        logging.info(f"number of messages {len(msgQueue)}")




