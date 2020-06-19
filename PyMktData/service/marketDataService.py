from PyMktData.model.Observer import MktDataObserver
from PyMktData.model.Subject import MarketDataSubject
import time
import abc
import random
import logging

class MarketDataInterface(abc.ABC):
  @abc.abstractmethod
  def connect(self):
    pass

  @abc.abstractmethod
  def disconnect(self):
    pass

  @abc.abstractmethod
  def subscribe(self, clientid, mktDataRequest, consumerFunc):
    pass

  @abc.abstractmethod
  def unsubscribe(self,  clientId, mktdatacode):
    pass

  @abc.abstractmethod
  def pollMarketData(self, mktdatacode):
    pass

import threading

def dummyfunc():
  while True:
    time.sleep(1)
    print("background run")

class DummyMarkDataImpl(MarketDataInterface):
  def __init__(self):
    self.min = 1
    self.max = 10
    self.subjectMap = {}
    self.isAlive = True

  def connect(self):
    logging.info("Connecting to market data server")
    self.bkThread = threading.Thread(target=self.___listenData, daemon=True)
    logging.info("Market data server connected")
    self.bkThread.start()

  def disconnect(self):
    logging.info("Market data server disconnected")
    self.isAlive = False

  def subscribe(self, clientId,  mktDataRequest, consumerFunc):
    mktdatacode = mktDataRequest["mktdatacode"]
    self.__addSubscription(clientId, mktdatacode, consumerFunc)


  def __addSubscription(self, clientId, mktdatacode, consumerFunc):
    mktdataObserver = MktDataObserver(clientId, consumerFunc, None)
    if mktdatacode not in self.subjectMap:
      self.subjectMap[mktdatacode] = MarketDataSubject(mktdatacode)
    self.subjectMap[mktdatacode].registerObserver(mktdataObserver)

  def unsubscribe(self,  clientId, mktdatacode):
    if mktdatacode in self.subjectMap:
      self.subjectMap[mktdatacode].removeObserver(clientId)
    else:
      raise Exception(f"mktdatacode {mktdatacode} not found")
  def ___listenData(self):

    while (self.isAlive):
      time.sleep(1)
      for mktdatacode in self.subjectMap.keys():
        logging.info(f"length of subjectmap {len(self.subjectMap)}")
        self.subjectMap[mktdatacode].notifyObservers(
          self.pollMarketData(mktdatacode)
        )
  def pollMarketData(self, mktdatacode):
    return {
            "Bid": random.random() * (self.max - self.min) + self.min,
            "Ask": random.random() * (self.max - self.min) + self.min
          }
