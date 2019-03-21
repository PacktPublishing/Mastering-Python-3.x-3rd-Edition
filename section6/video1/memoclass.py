class Memoize:
    def __init__(self, func):
        self.memos = {}
        self.func = func

    def __call__(self, *pargs, **kwargs):
        key = tuple([pargs, tuple(kwargs.items())])
        try:
            return self.memos[key]
        except KeyError:
            pass

        val = self.func(*pargs, **kwargs)
        self.memos[key] = val
        return val


@Memoize
def fibonacci(x):
    "Return the xth Fibonacci number"
    if x < 2:
        return x
    return fibonacci(x - 1) + fibonacci(x - 2)


if __name__ == '__main__':
    for i in range(10):
        print(fibonacci(i))
