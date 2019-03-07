import gevent
from gevent.queue import Queue
import requests
import time


__all__ = ["QUEUE", "geventIt"]


QUEUE = Queue()


def geventIt(func, number, urls=None, timeout=20, *arg, **kwargs):
    if urls != None:
        for u in urls:
            print(u)
            QUEUE.put_nowait(u)

    gevent.joinall(
        [gevent.spawn(func, *arg, **kwargs) for i in range(number)], timeout=timeout)
