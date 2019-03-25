__all__ = []


def power(x, y):
    ''' 实现一个数的平方 '''
    if y == 0:
        return 1
    if isinstance(y, int):
        k = x
        for i in range(y-1):
            x = x * k
    elif isinstance(y, float):
        x = x ** y
        # 现代计算机多采用移位法或牛顿迭代法
    return x
