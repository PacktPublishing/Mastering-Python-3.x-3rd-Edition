def memoize(func):
    memos = {}

    def wrapper(*pargs, **kwargs):
        key = tuple([pargs, tuple(kwargs.items())])
        try:
            return memos[key]
        except KeyError:
            pass

        val = func(*pargs, **kwargs)
        memos[key] = val
        return val

    return wrapper

@memoize
def fibonacci(x):
    "Return the xth Fibonacci number"
    if x < 2:
        return x
    return fibonacci(x - 1) + fibonacci(x - 2)


if __name__ == '__main__':
    for i in range(10):
        print(fibonacci(i))
