import asyncio
from contextlib import asynccontextmanager
from collections import ChainMap

@asynccontextmanager
async def transaction(data):
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

    async def __aenter__(self):
        return ChainMap(self.patch, self.data)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.data.update(self.patch)
        else:
            # We could return True if we wanted the exception to be considered handled
            return False


async def demo(context_manager):
    print('Demonstrating', context_manager.__name__)

    base = dict(foo = 1, bar = 2, baz = 3)

    try:
        async with context_manager(base) as data:
            data['foo'] = 17

            print(data['squack'])
    except KeyError:
        print('Got a key error, as expected')
        print('base is', base)

    try:
        async with context_manager(base) as data:
            data['foo'] = 17
    except KeyError:
        print('Got a key error, NOT expected')
    else:
        print('base is', base)

    print()


async def main():
    await demo(transaction)
    await demo(Transaction)

if __name__ == '__main__':
    asyncio.run(main())
