import gevent
from gevent.queue import Queue
import requests
import time


__all__ = ["Gevent"]

class Gevent():
    queue = Queue()

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def geventRun(self, func, number, urls=None, timeout=20, *arg, **kwargs):
        if urls != None:
            for u in urls:
                print(u)
                self.queue.put_nowait(u)

        gevent.joinall(
            [gevent.spawn(func, *arg, **kwargs) for i in range(number)], timeout=timeout)
