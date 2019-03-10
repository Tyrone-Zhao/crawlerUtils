import time
from selenium.common.exceptions import WebDriverException
from .base import BaseCrawler


__all__ = ["Decorator"]


MAX_WAIT = 10


class Decorator():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def wait(self, fn):
        ''' 装饰器，不断调用指定的函数，并捕获常规的异常，直到超时为止 '''
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    @classmethod
    def Singleton(self, cls):
        ''' 单例模式装饰器 '''
        _instance = {}

        def _singleton(*args, **kargs):
            if cls not in _instance:
                _instance[cls] = cls(*args, **kargs)
            return _instance[cls]

        return _singleton
