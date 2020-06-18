from typing import Dict

class MktDataObserver():
    def __init__(self, clientid, consumerFunc, throwFunc):
        self.clientid = clientid
        self.consumerFunc = consumerFunc
        self.throwFunc = throwFunc

    def update(self, msg:Dict):
        self.consumerFunc(msg)

    def throwError(self, throwable):
        self.throwFunc(throwable)
