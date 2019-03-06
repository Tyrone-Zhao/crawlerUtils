import gevent
from gevent.queue import Queue
import requests
import time


__all__ = ["QUEUE", "geventIt"]


QUEUE = Queue()


def geventIt(urls, number, func, *arg, **kwargs):
    for u in urls:
        QUEUE.put_nowait(u)

    gevent.joinall(
        [gevent.spawn(func, *arg, **kwargs) for i in range(number)])
