def printer(func):
    print(func)
    return func


def hello(x, y, z):
    return None


hello = printer(hello)
