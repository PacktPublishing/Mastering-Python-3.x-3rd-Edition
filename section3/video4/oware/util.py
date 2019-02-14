import io
import asyncio

class ByteFIFO:
    def __init__(self):
        self.data = bytearray()
        self.waiting = []

    def add(self, more):
        self.data.extend(more)

        waiting = self.waiting
        self.waiting = []
        for fut in waiting:
            fut.set_result(True)

        return self

    def remove(self, count):
        del self.data[:count]

    def as_file(self):
        return io.BytesIO(self.data)

    async def more_data(self):
        fut = asyncio.get_running_loop().create_future()
        self.waiting.append(fut)
        return await fut
