import time


__all__ = ["wait"]


MAX_WAIT = 10


def wait(fn):
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
