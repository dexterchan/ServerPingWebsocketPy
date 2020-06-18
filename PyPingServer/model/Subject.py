from PyPingServer.model.Observer import MktDataObserver

class MarketDataSubject():
    def __init__(self, mktdatacode):
        self.mktdatacode = mktdatacode
        self.observers = {}

    def notifyObservers(self, msg):
        for oberverKey in self.observers.keys():
            self.observers[oberverKey].update(msg)

    def registerObserver(self, observer:MktDataObserver):
        self.observers[observer.clientid] = observer


    def removeObserver(self, clientId):
        del self.observers[clientId]
