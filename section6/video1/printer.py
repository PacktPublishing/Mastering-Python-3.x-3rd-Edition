def printer(func):
    print(func)
    return func

@printer
def hello(x, y, z):
    return None
