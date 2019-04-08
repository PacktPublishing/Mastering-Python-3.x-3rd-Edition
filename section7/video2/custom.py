from contextlib import contextmanager
from collections import ChainMap

@contextmanager
def transaction(data):
    patch = {}
    try:
        yield ChainMap(patch, data)
    except:
        raise
    else:
        data.update(patch)


class Transaction:
    def __init__(self, data):
        self.data = data
        self.patch = {}

    def __enter__(self):
        return ChainMap(self.patch, self.data)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.data.update(self.patch)
        else:
            # We could return True if we wanted the exception to be considered handled
            return False


def demo(context_manager):
    print('Demonstrating', context_manager.__name__)

    base = dict(foo = 1, bar = 2, baz = 3)

    try:
        with context_manager(base) as data:
            data['foo'] = 17

            print(data['squack'])
    except KeyError:
        print('Got a key error, as expected')
        print('base is', base)

    try:
        with context_manager(base) as data:
            data['foo'] = 17
    except KeyError:
        print('Got a key error, NOT expected')
    else:
        print('base is', base)

    print()

if __name__ == '__main__':
    demo(transaction)
    demo(Transaction)
