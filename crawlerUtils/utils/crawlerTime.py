import time


__all__ = ["Time"]


class Time():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def timestamp_datetime(self, value):
        ''' 将Linux时间戳转化为2018-10-03 12:04:56类型的时间格式 '''
        # 将时间戳转换为time.struct_time()
        value = time.localtime(value)
        # 将time.struct_time()转换为时间格式
        format = '%Y-%m-%d %H:%M:%S'
        datetime = time.strftime(format, value)
        return datetime
