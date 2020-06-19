import queue
class BlockingQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def insertItem(self, msg):
        self.queue.put(msg, block=True)

    def consumeItem(self, timeoutSeconds=None):
        return self.queue.get(block=True, timeout = timeoutSeconds)