import unittest
from PyMktData.model.Observer import MktDataObserver
from PyMktData.model.Subject import MarketDataSubject

from collections import deque

msgQueue = deque()

def consumerFunc(msg):
    msgQueue.append(msg)

def throwFunc(msg):
    print("throw:"+msg)

class MarketDataSubjectSuite(unittest.TestCase):



    def test_insertSubject(self):
        mktdatacode = "AAPL 150117C00600000 EQUITY"
        mktDataObserver =  MktDataObserver("abcd",consumerFunc, throwFunc)
        mktDataObserver2 = MktDataObserver("def", consumerFunc, throwFunc)
        marketDataSubject = MarketDataSubject(mktdatacode)
        marketDataSubject.registerObserver(mktDataObserver)
        marketDataSubject.registerObserver(mktDataObserver2)

        msg = {
            "Bid": 1,
            "Ask": 1
        }
        marketDataSubject.notifyObservers(msg)
        self.assertEqual(1*2, len(msgQueue))
        marketDataSubject.notifyObservers(msg)
        self.assertEqual(2*2, len(msgQueue))
        marketDataSubject.removeObserver(mktDataObserver2.clientid)
        marketDataSubject.notifyObservers(msg)
        self.assertEqual(2 * 2+1, len(msgQueue))