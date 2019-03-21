import random
import functools

def clamp(low_bound, high_bound):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*pargs, **kwargs):
            val = func(*pargs, **kwargs)
            val = max(val, low_bound)
            val = min(val, high_bound)
            return val
        return wrapper
    return deco


def square(func):
    @functools.wraps(func)
    def wrapper(*pargs, **kwargs):
        return func(*pargs, **kwargs) ** 2
    return wrapper

@square
@clamp(10, 50)
def do_that_thing():
    return random.randrange(100)


if __name__ == "__main__":
    for i in range(10):
        print(do_that_thing())
